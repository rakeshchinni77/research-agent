# Autonomous Research Agent

A production-ready autonomous research agent built with **LangChain**, **FastAPI**, **Redis**, and **SQLite**. The agent follows the **ReAct** (Reasoning + Acting) pattern, using a set of pluggable tools to answer complex, multi-step queries.

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Tools](#tools)
5. [Setup — Local (without Docker)](#setup--local-without-docker)
6. [Setup — Docker](#setup--docker)
7. [API Reference](#api-reference)
8. [Running Tests](#running-tests)
9. [Environment Variables](#environment-variables)

---

## Features

- **ReAct agent loop** — the LLM reasons step-by-step, selects a tool, observes the result, and iterates.
- **4 built-in tools** — calculator, web search, SQL query, Python code interpreter.
- **Redis conversation memory** — multi-turn sessions with full history retrieval.
- **SQLite database** — pre-seeded with a `users` table for SQL tool demos.
- **REST API** — a single `/agent/invoke` endpoint returns the final answer plus a full reasoning trace.
- **Graceful fallback** — if the OpenAI API is unavailable or rate-limited, a deterministic tool dispatcher handles all standard queries without an LLM call.
- **Docker-ready** — fully containerised with a `docker-compose.yml` that starts the app and Redis, runs the seed script, and exposes health checks.

---


> 🚀 Live Demo: See the agent in action → [Watch Video](https://drive.google.com/file/d/1uhzKfTdwDoWu-cEFWNQovOq5v9HPpEyP/view)

---

# Architecture

The system follows a **modular architecture** where the **LLM agent orchestrates multiple tools** and stores conversation history in Redis.

```
User
 |
 v
FastAPI API
 |
 v
LangChain ReAct Agent
 |
 +---- Calculator Tool
 |
 +---- Web Search Tool (SerpAPI)
 |
 +---- SQL Query Tool (SQLite)
 |
 +---- Python Code Interpreter
 |
 v
Redis (Conversation Memory)
 |
 v
SQLite Database
```

---

## Components

| Component | Description |
|----------|-------------|
| FastAPI | REST API to interact with the agent |
| LangChain | Handles agent reasoning and tool execution |
| Redis | Stores conversation history using session IDs |
| SQLite | Local database storing users table |
| Docker | Containerized deployment |
| SerpAPI | Web search integration |

---
---

## Project Structure

```
research-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py            # ReAct agent loop + fallback dispatcher
│   ├── main.py             # FastAPI app — /health + /agent/invoke
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py           # SQLite connection helper
│   ├── memory/
│   │   ├── __init__.py
│   │   └── redis_memory.py # save/get/clear conversation history
│   └── tools/
│       ├── __init__.py
│       ├── calculator.py
│       ├── web_search.py
│       ├── sql_tool.py
│       └── python_interpreter.py
├── tests/
│   ├── __init__.py
│   ├── test_agent.py
│   └── test_tools.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── seed.py                 # Idempotent DB seeder (INSERT OR IGNORE)
├── .env.example
└── README.md
```

---

## Tools

| Tool | Description | Input |
|------|-------------|-------|
| `calculator` | Evaluates arithmetic/math expressions via `eval()` | `"0.375 * 800"` |
| `web_search` | Google search via SerpAPI; returns top snippet | `"capital of France"` |
| `sql_query_tool` | Executes a SQL `SELECT` on the SQLite database | `"SELECT COUNT(*) FROM users"` |
| `python_code_interpreter` | Runs Python code; returns the `result` variable | `"result = sum(range(6))"` |

---

## Setup — Local (without Docker)

### Prerequisites

- Python 3.10+
- Redis running on `localhost:6379` (or set `REDIS_HOST`)
- SerpAPI account for web search (optional — skip by omitting `SEARCH_API_KEY`)
- OpenAI API key

### Steps

```bash
# 1. Clone the repo
git clone "https://github.com/rakeshchinni77/research-agent"
cd research-agent

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
copy .env.example .env      # Windows
# cp .env.example .env      # macOS/Linux
# Edit .env with your API keys

# 5. Seed the database
python seed.py

# 6. Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API is now available at `http://localhost:8000`.

---

## Setup — Docker

### Prerequisites

- Docker Desktop (or Docker Engine + Compose)
- A configured `.env` file (copy from `.env.example` and fill in your keys)

### Steps

```bash
# 1. Configure environment variables
copy .env.example .env
# Edit .env with your OPENAI_API_KEY and SEARCH_API_KEY

# 2. Start all services
docker-compose up --build

# The app will:
#   • Build the Python image
#   • Start Redis
#   • Run seed.py to create and populate the database
#   • Start uvicorn on port 8000

# 3. Verify health
curl http://localhost:8000/health
# → {"status": "ok"}
```

To stop:

```bash
docker-compose down
```

---

## API Reference

### `GET /health`

Returns the service health status.

**Response:**
```json
{"status": "ok"}
```

---

### `POST /agent/invoke`

Invoke the research agent with a natural-language query.

**Request body:**
```json
{
  "query": "What is 37.5% of 800?",
  "session_id": "my-session-123"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | The question or task for the agent |
| `session_id` | string | Yes | Unique identifier for the conversation (enables multi-turn memory) |

**Response:**
```json
{
  "response": "37.5% of 800 is 300.",
  "reasoning_trace": [
    {
      "thought": "I should use the calculator for percentage arithmetic.",
      "action": "calculator",
      "observation": "300.0"
    }
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `response` | string | Final answer from the agent |
| `reasoning_trace` | array | Ordered list of thought / action / observation steps |

**Example queries:**

```bash
# Math
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 37.5% of 800?", "session_id": "s1"}'

# SQL
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "How many users are in the database?", "session_id": "s2"}'

# Python execution
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the first 5 square numbers starting from 1?", "session_id": "s3"}'

# Web search
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?", "session_id": "s4"}'

# Multi-step (SQL + calculator)
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "Find the number of users in the database and multiply it by 15 * 4", "session_id": "s5"}'
```

---

## Running Tests

```bash
# Activate your virtual environment first
venv\Scripts\activate    # Windows

# Run all tests
python -m pytest tests/ -v

# Run only tool tests (no LLM required)
python -m pytest tests/test_tools.py -v

# Run only agent tests
python -m pytest tests/test_agent.py -v
```

> **Note:** `test_tools.py` includes `web_search` tests that require a valid `SEARCH_API_KEY` environment variable. All other tests work with a seeded `research_agent.db` and a locally running Redis instance (or no Redis — the memory module falls back gracefully).

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | Yes | — | OpenAI API key (gpt-4o-mini used by default) |
| `SEARCH_API_KEY` | Yes | — | SerpAPI key for web search tool |
| `DATABASE_URL` | No  | `sqlite:///./research_agent.db` | SQLite database URL |
| `REDIS_HOST` | No | `redis` (Docker) / `localhost` (local) | Redis hostname |
| `REDIS_PORT` | No | `6379` | Redis port |
| `REDIS_DB` | No | `0` | Redis database index |
| `API_PORT` | No | `8000` | Port for the FastAPI server |

---
#  Testing

Run tests using:

```bash
pytest
```

---

##  Expected Result

```
9 passed
```

---

## Test Coverage

The test suite covers the following components:

- **Calculator Tool**
- **Web Search Tool**
- **SQL Tool**
- **Python Interpreter**
- **Agent Reasoning**
- **Multi-step Tool Usage**

---
