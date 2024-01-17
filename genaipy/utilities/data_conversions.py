"""Submodule for data conversion utilities."""

import json
import logging
import pandas as pd


def convert_json_to_df(json_str: str) -> pd.DataFrame:
    """
    Converts a JSON string to a pandas DataFrame.

    Args:
        json_str (str): A JSON string to be converted.

    Returns:
        pd.DataFrame: DataFrame representation of the JSON string.

    Raises:
        ValueError: If the JSON string cannot be parsed.
    """
    try:
        data = json.loads(json_str)
        df = pd.DataFrame.from_dict(data, orient="index")
        return df
    except json.JSONDecodeError as e:
        logging.error("JSON parsing error: %s", e)
        raise ValueError(f"Invalid JSON string: {e}") from e
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        raise


def convert_df_to_messages(
    df: pd.DataFrame, system_msg: str, user_col: str, assistant_col: str
) -> list:
    """
    Converts a DataFrame to a list of message dictionaries.

    Args:
        df (pd.DataFrame): DataFrame containing messages.
        system_msg (str): System message to be included in each entry.
        user_col (str): Column name for user messages.
        assistant_col (str): Column name for assistant messages.

    Returns:
        list: List of message dictionaries.

    Raises:
        ValueError: If the DataFrame does not contain the required columns.
    """
    if not {user_col, assistant_col}.issubset(df.columns):
        logging.error("Missing required columns in DataFrame.")
        raise ValueError("DataFrame must contain specified user and assistant columns.")

    try:
        output = []
        for _, row in df.iterrows():
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
        logging.error("Error in converting DataFrame to messages: %s", e)
        raise
