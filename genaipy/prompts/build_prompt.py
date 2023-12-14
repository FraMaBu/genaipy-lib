"""Module for functions building prompts from templates."""

import logging


def build_prompt(template: str, **kwargs) -> str:
    """Builds a prompt from a template and provided keyword arguments.

    Args:
        template (str): The template string with placeholders for formatting.
        **kwargs: Keyword arguments that correspond to placeholders in the template.

    Returns:
        str: A string with the placeholders in the template filled with provided arguments.

    Raises:
        KeyError: If a placeholder in the template does not have a corresponding keyword argument.

    Note:
        The function handles extra, unused arguments gracefully by ignoring them.
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logging.error(
            "Missing required argument for placeholder '%s' in the template.", e.args[0]
        )
        raise
