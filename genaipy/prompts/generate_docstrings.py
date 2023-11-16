"""Module for generating docstrings prompt templates and prompt builder function."""


GENERATE_DOCSTRING_TPL = """
Function:
```{function}```

Instructions:
Write a {style}-style docstring including type annotations for the provided function.
Only return the final function in your response. 
"""


def build_docstring_prompt(
    function: str, style: str = "Google", template: str = GENERATE_DOCSTRING_TPL
) -> str:
    """Builds docstring prompt from prompt template and inputs.

    Args:
        function (str): The function to generate a docstring for.
        style (str, optional): The style of the docstring to generate. Defaults to "Google".
            Recommended values 'Google', 'PEP 257', 'Numpy', or 'Sphynx'.
        template (str, optional): Prompt template to use, must contatin placeholders for
            all variables. Defaults to GENERATE_DOCSTRING_TPL.

    Returns:
        str: A formatted docstring prompt for the specified function and style.
    """
    return template.format(function=function, style=style)
