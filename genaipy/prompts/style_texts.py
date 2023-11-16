"""Module for style text prompt templates and prompt builder function."""

STYLE_TEXT_TPL = """
Text:
{text}

Instructions:
Transform the provided text into the provided outline enclosed by triple back ticks.

Outline:
```{tpl}```

Only return the final, filled outline in your response.
"""


def build_style_prompt(
    text: str,
    tpl: str,
    template=STYLE_TEXT_TPL,
) -> str:
    """Build style text prompt from text input, layout template, and prompt template.

    Args:
        text (str): Text sample to style.
        tpl (str): Template of layout.
        template (str, optional): prompt template to use, ust contain placeholders for
            all variables. Defaults to `STYLE_TEXT_TPL`.

    Returns:
        str: Prepared prompt
    """
    return template.format(text=text, tpl=tpl)
