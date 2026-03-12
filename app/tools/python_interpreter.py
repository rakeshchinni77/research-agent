def python_code_interpreter(code: str) -> str:
    """
    Executes Python code and returns the output.
    """

    try:
        # Create a restricted local environment
        local_vars = {}

        # Execute the Python code
        exec(code, {}, local_vars)

        # If the code defines a variable called 'result', return it
        if "result" in local_vars:
            return str(local_vars["result"])

        # Otherwise return all local variables
        return str(local_vars)

    except Exception as e:
        return f"Python execution error: {str(e)}"