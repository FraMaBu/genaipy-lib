"""Module for QA generation prompt templates and prompt builder function."""

GENERATE_QA_TPL = """
Text sample:
```{text}```

Instructions:
Your task is to generate {num} detailed question-answer pairs for the provided text sample.
Make sure that the question-answer pairs are self-contained and detailed so users do not need to search outside to understand the answer.

Answer in JSON. The JSON object must consist of {num} dictionaries whose keys are "question" and "answer".
Do not provide any additional information except the JSON.
"""


def build_qa_prompt(text: str, num: int = 5, template=GENERATE_QA_TPL) -> str:
    """
    Builds a QA generation prompt using the given text sample and inputs.

    Args:
        text (str): The text sample to use as the basis for generating questions.
        num (int, optional): The number of question-answer pairs to generate. Defaults to 5.
        template (str, optional): The template to use for generating the QA prompt.
            Defaults to GENERATE_QA_TPL.

    Returns:
        str: The prepared QA prompt.

    Note:
        This prompt is designed to be used with JSON-mode enabled (see OpenAI Chat API).
    """
    return template.format(text=text, num=num)
