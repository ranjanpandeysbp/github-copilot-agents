"""
calculator.py - Tool for performing basic arithmetic operations: addition,
subtraction, multiplication, and division.
"""

def calculate(expression: str) -> str:
    """
    Parses a simple arithmetic expression (e.g., '7+8', '10-3', '4*5', '20/4')
    and returns a formatted result string.

    Supported operators: +, -, *, /
    """

    print(f"[LOG] calculate() called with expression: '{expression}'")

    import re

    match = re.fullmatch(
        r"\s*(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)\s*",
        expression
    )

    if not match:
        print("[LOG] Invalid expression format or unsupported operation.")
        return (
            "Error: Unsupported operation or invalid format. "
            "Please enter an expression with two numbers and one of the following operators: +, -, *, / (e.g., '7+8', '10-3', '4*5', '20/4')."
        )

    a, op, b = match.groups()

    a = float(a) if "." in a else int(a)
    b = float(b) if "." in b else int(b)

    if op == "+":
        result = a + b
        print(f"[LOG] Addition: {a} + {b} = {result}")
        return f"Result of Addition for {a} and {b} is {result}"

    elif op == "-":
        result = a - b
        print(f"[LOG] Subtraction: {a} - {b} = {result}")
        return f"Result of Subtraction for {a} and {b} is {result}"

    elif op == "*":
        result = a * b
        print(f"[LOG] Multiplication: {a} * {b} = {result}")
        return f"Result of Multiplication for {a} and {b} is {result}"

    elif op == "/":
        if b == 0:
            print("[LOG] Division by zero attempted.")
            return "Error: Division by zero is not allowed."

        result = a / b
        print(f"[LOG] Division: {a} / {b} = {result}")
        return f"Result of Division for {a} and {b} is {result}"
    else:
        print("[LOG] Unsupported operation encountered.")
        return (
            "Error: Unsupported operation or invalid format. "
            "Please enter an expression with two numbers and one of the following operators: +, -, *, / "
            "(e.g., 7+8, 10-3, 4*5, 20/4)."
        )