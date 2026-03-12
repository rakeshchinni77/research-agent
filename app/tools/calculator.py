from langchain_core.tools import Tool


def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression and return the result.
    """

    try:
        result = eval(expression)
        return str(result)

    except Exception as e:
        return f"Calculation error: {str(e)}"


calculator_tool = Tool(
    name="calculator",
    func=calculate,
    description=(
        "Useful for performing mathematical calculations. "
        "Input should be a valid mathematical expression like "
        "'15 * 4' or '0.375 * 800'."
    ),
)