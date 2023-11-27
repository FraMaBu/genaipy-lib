""" Module for summary prompt templates and prompt builder function."""

SUMMARY_PROMPT_TPL = """
Text sample:
```{text}```

Instructions:
Your task is to generate a summary of the text sample.
Summarize the provided text sample, delimited by triple backticks, in at most {max_words} words.

Summarized text:
"""

REDUCE_SUMMARY_PROMPT_TPL = """
Text samples:
```{text}```

Instructions:
Your task is to distill the provided set of text samples, delimited by triple back ticks, into a final, consolidated summary in at most {max_words} words.
Make sure that the final summary is coherent and clearly structured by using headings, paragraphs, and bulleted lists.

Final summary:
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
