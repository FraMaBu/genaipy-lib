"""Module for QA generation prompt templates and system messages."""

GENERATE_QA_TPL = """
Text sample:
```{text}```

Instructions:
Your task is to generate {num} detailed question-answer pairs for the provided text sample.
Make sure that the question-answer pairs are self-contained and detailed so users do not need to search outside to understand the answer.

Answer in JSON. The JSON object must consist of {num} dictionaries whose keys are "question" and "answer".
Do not provide any additional information except the JSON.
"""
