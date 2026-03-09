---
description: Tool for performing basic arithmetic operations (addition, subtraction, multiplication, division) using calculator.py.
entrypoint: calculator.py:calculate
name: calculator_tool
inputs:
  - name: expression
    type: string
    description: Simple arithmetic expression (e.g., 7+8, 10-3, 4*5, 20/4)
outputs:
  - name: result
    type: string
    description: Result string describing the operation and result, or an error message.
---

This tool exposes the calculate() function from calculator.py. It takes an arithmetic expression as input and returns a formatted result string. Only +, -, *, / are supported.