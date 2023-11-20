""" Module for summary prompt templates and prompt builder function."""

SUMMARY_PROMPT_TPL = """
Instructions:
Your task is to generate a summary of the text sample.
Summarize the text sample provided below, delimited by triple backticks, in at most {max_words} words.

Text sample:
```{text}```

Summarized text:
"""


def build_summary_prompt(
    text: str, max_words: int = 150, template: str = SUMMARY_PROMPT_TPL
) -> str:
    """Builds summary prompt from template and input.

    Args:
        text (str): text sample to summarize.
        max_words (int, optional): Maximum number of summary words, by default 150.
        template (str, optional): Prompt template to use, must contain placeholders for
            all variables. Defaults to `SUMMARY_PROMPT_TEMPLATE`.

    Returns:
        str: Prepared prompt.
    """
    return template.format(text=text, max_words=max_words)
