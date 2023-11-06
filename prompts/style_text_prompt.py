"""Module for style text prompt template and prompt builder function"""

STYLE_TEXT_PROMPT_TEMPLATE = """
Text:
{text}

Instructions:
Transform the provided text into the provided outline enclosed by triple back ticks.

Outline:
```
{tpl}
```

Provide your response in {output_type}. Only return the final, filled outline in your response.
"""


def build_style_text_prompt(
    text: str,
    tpl: str,
    output_type: str = "markdown",
    template=STYLE_TEXT_PROMPT_TEMPLATE,
) -> str:
    """Build style text prompt from text input, layout template, and prompt template.

    Args:
    - text (str): Text to style
    - tpl (str): Template of layout
    - output_type (str): Desired output format. Defaults to 'markdown'.
    - template: prompt template to use, ust contain placeholders for all variables.
                Defaults to STYLE_DRAFT_PROMPT_TEMPLATE.

    Returns:
    - str: prepared prompt
    """
    return template.format(text=text, tpl=tpl, output_type=output_type)
