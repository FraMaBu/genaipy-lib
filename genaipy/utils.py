"""Module for helper functions."""

import json
import logging
import os

import pandas as pd


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
    permissible_env_vars = {"OPENAI_API_KEY"}  # TODO: Extend set if relevant

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


def convert_json_to_df(json_str: str) -> pd.DataFrame:
    """
    Converts a JSON string containing dictionaries with an arbitrary number of
    key-value pairs into a pandas DataFrame.

    Each key in the JSON object represents a dictionary with 'n' number of keys.
    The function parses this JSON string and extracts these dictionaries into a DataFrame.

    Args:
        json_str (str): A JSON string containing dictionaries, each with any number of keys.

    Returns:
        pd.DataFrame: A DataFrame where each row corresponds to a dictionary from the JSON object.
            The DataFrame will have dynamic columns based on the keys in the JSON dictionaries.

    Raises:
        ValueError: If the JSON string cannot be parsed.

    Example:
        >>> test_json = '{"1": {"key1": "value1", "key2": "value2"}, "2": {"key1": "value3", "key2": "value4"}}'
        >>> dataframe = json_to_dataframe(test_json)
        >>> dataframe.loc['1', 'key1']
        'value1'
        >>> dataframe.loc['2', 'key2']
        'value4'
    """
    try:
        # Parsing the JSON string
        data = json.loads(json_str)

        # Creating DataFrame directly from the JSON data
        df = pd.DataFrame.from_dict(data, orient="index")

        return df

    except json.JSONDecodeError as e:
        logging.error("Error parsing JSON: %s", e)
        raise ValueError(f"Invalid JSON string: {e}")

    except Exception as e:
        logging.error("Unexpected error: %s", e)
        raise


def convert_df_to_messages(
    df: pd.DataFrame, system_msg: str, user_col: str, assistant_col: str
) -> list:
    """
    Converts a DataFrame containing user and assistant messages into a list of dictionaries.

    This function is mainly used to convert a fine-tuning dataset to the format required
    by the `OpenAI fine-tuning API`.

    Args:
        df (pd.DataFrame): DataFrame containing the messages.
        system_msg (str): System message to be included in each entry.
        user_col (str): The name of the column containing user messages.
        assistant_col (str): The name of the column containing assistant messages.

    Returns:
        list: A list of dictionaries representing the messages in the specified format.

    Raises:
        ValueError: If the DataFrame does not contain the required columns.
    """

    # Verify DataFrame has required columns
    if not {user_col, assistant_col}.issubset(df.columns):
        logging.error(
            "DataFrame must contain columns '%s' and '%s'.", user_col, assistant_col
        )
        raise ValueError(
            f"DataFrame must contain columns '{user_col}' and '{assistant_col}'."
        )

    try:
        output = []
        for _, row in df.iterrows():  # do not use index
            message = {
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": row[user_col]},
                    {"role": "assistant", "content": row[assistant_col]},
                ]
            }
            output.append(message)

        return output
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        raise


def write_to_jsonl_file(data: list, output_path: str = "output.jsonl") -> None:
    """
    Writes a list of dictionaries to a file in JSON Lines format.

    The resulting output file will be in JSONL format, as required
    by the `OpenAI Fine-tuning API`.

    Args:
        data (list): The list of dictionaries to be written to the file.
            Defaults to 'output.jsonl'
        filename (str): The name of the file to write.

    Raises:
        Exception: For any errors that occur during file writing.
    """

    try:
        with open(output_path, "w", encoding="utf-8") as file:
            for item in data:
                json.dump(item, file)
                file.write("\n")
        logging.info("Data successfully written to %s", output_path)

    except Exception as e:
        logging.error("An error occurred while writing to file: %s", e)
        raise
