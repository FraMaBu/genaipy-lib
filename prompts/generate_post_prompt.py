"""Module for generate social media post prompt template and prompt builder function."""

GENERATE_POST_PROMPT_TEMPLATE = """
Text sample:
```{text}```

Instructions:
Your task is to generate an engaging {platform} post about the provided text sample delimited by triple back ticks.

Guidelines:
- Clearly structure the post by using headings, paragraphs, and bulleted lists. 
- Write the post in first person.
- Limit your post to at most {max_words} words.

 Only return the engaging post in your response and nothing else.
"""


def build_generate_post_prompt(
    text: str,
    max_words: int = 120,
    platform: str = "LinkedIn",
    template: str = GENERATE_POST_PROMPT_TEMPLATE,
) -> str:
    """Builds basic summary prompt from template and input.

    Args:
    - text (str): Text sample to generate post.
    - max_words (str, optional): Maximum number of post words. Defaults to 100.
    - platform (str, optional): The social media platform the post is intended for.
        Defaults to 'LinkedIn'.
    - template (str, optional): Prompt template to use, must contain placeholders for all variables.
        Defaults to `GENERATE_POST_PROMPT_TEMPLATE`.

    Returns:
    - str: Prepared prompt.
    """
    return template.format(text=text, max_words=max_words, platform=platform)
