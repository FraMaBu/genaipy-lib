"""Module for coding related prompt templates and system messages."""

DEFAULT_SYS_MSG = """
You are a world-class Python developer with an eagle eye for unintended bugs and edge cases. You carefully explain code with great detail and accuracy.
"""

EXPLAIN_FUN_TPL = """
Function:
```{function}```

Instructions:
Please explain the provided {language} function delimited by tripple back ticks.
Review what each element of the function is doing precisely and what the author's intentions may have been.

Explanation:
"""

PLAN_TEST_TPL = """
Function:
{function}

Guidelines:
A good unit test suite should aim to:
- Test the function's behavior for a wide range of possible inputs
- Test edge cases that the author may not have foreseen
- Take advantage of the features of `{unit_test_package}` to make the tests easy to write and maintain
- Be easy to read and understand, with clean code and descriptive names
- Be deterministic, so that the tests always pass or fail in the same way

Instructions:
Unit test the function above, list diverse scenarios that the function should be able to handle (and under each scenario, include a few examples as sub-bullets).
"""
