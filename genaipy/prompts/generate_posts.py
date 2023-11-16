"""Module for social media post prompt templates and prompt builder function."""

GENERATE_POST_TPL = """
Text sample:
```{text}```

Instructions:
Your task is to generate an engaging post about the provided text sample delimited by triple back ticks.

Guidelines:
- Clearly structure the post by using headings, paragraphs, and bulleted lists. 
- Write the post in first person.
- Limit your post to at most {max_words} words.

 Only return the engaging post in your response and nothing else.
"""


def build_post_prompt(
    text: str,
    max_words: int = 120,
    template: str = GENERATE_POST_TPL,
) -> str:
    """Builds summary prompt from prompt template and inputd.

    Args:
        text (str): Text sample to generate post.
        max_words (str, optional): Maximum number of post words. Defaults to 100.
        template (str, optional): Prompt template to use, must contain placeholders for
            all variables. Defaults to `GENERATE_POST_TPL`.

    Returns:
        str: Prepared prompt.
    """
    return template.format(text=text, max_words=max_words)
