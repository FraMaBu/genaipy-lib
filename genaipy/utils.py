"""Module for helper functions."""

import logging
import os


def save_string_txt(string: str, output_path: str) -> bool:
    """
    Saves the given string as a text file at the output path with UTF-8 encoding.

    Args:
        string (str): The string to be saved as a text file.
        output_path (str): The path where the text file should be saved.

    Returns:
        bool: Status indicator. True if the file is successfully saved, False otherwise.

    Raises:
        Exception: Propagates any exceptions that occur during file writing.

    """
    if not isinstance(string, str):
        logging.error("Provided input is not a string.")
        return False
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(string)
        return True
    except Exception as e:
        logging.error("Error occurred while saving file at %s: %s", output_path, e)
        raise


def validate_api_key(env_var_name: str = "OPENAI_API_KEY") -> str:
    """
    Validates if the specified environment variable for the API key is set and permissible.

    Args:
        env_var_name (str): Name of the environment variable to check.
            Defaults to 'OPENAI_API_KEY'.

    Returns:
        str: The value of the specified API key.

    Raises:
        ValueError: If the environment variable name is not permissible or the key is not set.
    """
    permissible_env_vars = {"OPENAI_API_KEY"}

    if env_var_name not in permissible_env_vars:
        logging.error("Invalid environment variable name: %s", env_var_name)
        raise ValueError(
            f"Environment variable '{env_var_name}' is not a permissible key name."
        )

    api_key = os.environ.get(env_var_name)

    if not api_key:
        logging.error("Environment variable not set: '%s'.", env_var_name)
        raise ValueError(f"Environment variable '{env_var_name}' is not set.")

    return api_key
