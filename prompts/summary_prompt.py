""" Module for basic summary prompt template and prompt builder function."""

SUMMARY_PROMPT_TEMPLATE = """
Instructions:
Your task is to generate a summary of the text sample.
Summarize the text sample provided below, delimited by triple backticks, in at most {max_words} words.

Text sample:
```{text}```

Summarized text:
"""


def build_summary_prompt(
    text: str, max_words: int = 150, template: str = SUMMARY_PROMPT_TEMPLATE
) -> str:
    """Builds basic summary prompt from template and input.

    Args:
    - text (str): text sample to summarize.
    - max_words (str, optional): Maximum number of summary words, by default 150.
    - template (str, optional): Prompt template to use, must contain placeholders for all variables,
        by default `SUMMARY_PROMPT_TEMPLATE`.

    Returns:
    - str: Prepared prompt.
    """
    return template.format(text=text, max_words=max_words)
