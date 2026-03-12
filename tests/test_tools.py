import pytest

from app.tools.calculator import calculate
from app.tools.web_search import web_search
from app.tools.sql_tool import sql_query_tool
from app.tools.python_interpreter import python_code_interpreter


def test_calculator():
    result = calculate("0.375 * 800")
    assert float(result) == 300.0


def test_web_search():
    result = web_search("What is the capital of France?")
    assert "paris" in result.lower()


def test_sql_query_tool():
    result = sql_query_tool("SELECT COUNT(*) AS count FROM users;")

    # result example: "[{'count': 3}]"
    assert "count" in result
    assert "3" in result


def test_python_interpreter():
    code = "result = ', '.join(str(i*i) for i in range(1,6))"
    result = python_code_interpreter(code)

    assert "1" in result
    assert "4" in result
    assert "9" in result
    assert "16" in result
    assert "25" in result