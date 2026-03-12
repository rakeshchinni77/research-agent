from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from app.agent import invoke_agent


# Create FastAPI app
app = FastAPI(
    title="Autonomous Research Agent API",
    description="AI agent capable of reasoning and using tools",
    version="1.0"
)


# Request schema
class AgentRequest(BaseModel):
    query: str
    session_id: str


# Reasoning trace schema
class ReasoningStep(BaseModel):
    thought: str
    action: str
    observation: str


# Response schema
class AgentResponse(BaseModel):
    response: str
    reasoning_trace: List[ReasoningStep]


# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}


# Agent invocation endpoint
@app.post("/agent/invoke", response_model=AgentResponse)
def invoke(request: AgentRequest):

    try:
        result = invoke_agent(
            query=request.query,
            session_id=request.session_id
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))