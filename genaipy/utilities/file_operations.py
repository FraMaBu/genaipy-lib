"""Submodule for file operations."""

import json
import logging


def write_string_to_txt(text: str, file_path: str = "output.txt") -> bool:
    """
    Saves the given text string to a file with UTF-8 encoding.

    Args:
        text (str): The text string to be saved.
        file_path (str): The path where the file should be saved.

    Returns:
        bool: True if the file is successfully saved, False otherwise.

    Raises:
        Exception: If an error occurs during file writing.
    """
    if not isinstance(text, str):
        logging.error("Input text is not a string.")
        return False
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)
        return True
    except Exception as e:
        logging.error("Error saving file at '%s': %s", file_path, e)
        raise


def write_data_to_jsonl(data: list, file_path: str = "output.jsonl") -> None:
    """
    Writes a list of dictionaries to a JSON Lines format file.

    Args:
        data (list): List of dictionaries to be written.
        jsonl_path (str): Path of the JSON Lines format file.

    Raises:
        Exception: If an error occurs during file writing.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for item in data:
                json.dump(item, file)
                file.write("\n")
        logging.info("Data written to JSON Lines file '%s'", file_path)

    except Exception as e:
        logging.error("Error writing to JSON Lines file '%s': %s", file_path, e)
        raise
