"""Module for helper functions"""

import logging


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
        logging.info("File successfully saved at %s", output_path)
        return True
    except Exception as e:
        logging.error("Error occurred while saving file at %s: %s", output_path, e)
        raise
