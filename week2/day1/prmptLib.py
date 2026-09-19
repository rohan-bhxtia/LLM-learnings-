CALCULATE_TOOL = {
    "name": "calculate",
    "description": (
        "Performs one arithmetic operation (add, subtract, multiply, divide) "
        "on two numbers. Use this any time exact arithmetic is needed — "
        "never compute math yourself."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
            },
            "a": {"type": "number", "description": "The first number"},
            "b": {"type": "number", "description": "The second number"},
        },
        "required": ["operation", "a", "b"],
    },
}

def calculate(operation: str, a: float, b: float) -> float:
    """The REAL function that actually does the math."""
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    raise ValueError(f"Unknown operation: {operation}")