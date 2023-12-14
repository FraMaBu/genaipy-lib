"""Module for generating docstrings prompt templates and system messages."""


GENERATE_DOCSTRING_TPL = """
Function:
```{function}```

Instructions:
Write a {style}-style docstring including type annotations for the provided function.
Only return the final function in your response.

Final function:
"""
