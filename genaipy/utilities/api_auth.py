# api_interaction.py
"""Submodule for API authentification."""

import os
import logging


def validate_api_key(env_var_name: str = "OPENAI_API_KEY") -> str:
    """
    Validates if the specified environment variable for the API key is set and valid.

    Args:
        env_var_name (str): Name of the environment variable to check.
            Defaults to 'OPENAI_API_KEY'.

    Returns:
        str: The value of the API key.

    Raises:
        ValueError: If the environment variable is not permissible or not set.
    """
    permissible_env_vars = {"OPENAI_API_KEY"}  # TODO: Extend set if relevant

    if env_var_name not in permissible_env_vars:
        logging.error("Invalid environment variable name: '%s'", env_var_name)
        raise ValueError(
            f"Environment variable '{env_var_name}' is not a permissible key name."
        )

    api_key = os.environ.get(env_var_name)

    if not api_key:
        logging.error("Environment variable not set: '%s'", env_var_name)
        raise ValueError(f"Environment variable '{env_var_name}' is not set.")

    return api_key
