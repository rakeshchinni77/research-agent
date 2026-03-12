from app.agent import invoke_agent


def test_calculator_reasoning():
    result = invoke_agent(
        "What is 37.5% of 800?",
        "pytest-session-1"
    )

    assert "300" in result["response"]
    assert len(result["reasoning_trace"]) > 0
    assert result["reasoning_trace"][0]["action"] == "calculator"


def test_web_search_reasoning():
    result = invoke_agent(
        "What is the capital of France?",
        "pytest-session-2"
    )

    assert "paris" in result["response"].lower()


def test_sql_reasoning():
    result = invoke_agent(
        "How many users are in the database?",
        "pytest-session-3"
    )

    assert "3" in result["response"]


def test_python_reasoning():
    result = invoke_agent(
        "What are the first 5 square numbers starting from 1?",
        "pytest-session-4"
    )

    assert "1" in result["response"]
    assert "25" in result["response"]


def test_multi_step_reasoning():
    result = invoke_agent(
        "Find the number of users in the database and multiply it by the result of 15 * 4",
        "pytest-session-5"
    )

    assert "180" in result["response"]
    assert len(result["reasoning_trace"]) >= 2