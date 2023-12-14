"""Module for interfacing with the OpenAI Chat API"""

import logging
import time
from typing import Any
import openai


# Custom Exceptions for Chat API
class ChatAPIRequestException(Exception):
    """Exception raised for errors in the OpenAI Chat API request process."""


class ChatAPIResponseException(Exception):
    """Exception raised for errors in processing the OpenAI Chat API response."""


# Functions for interfacing with Chat API
def construct_chat_message(role: str, content: str) -> dict:
    """
    Constructs a message for OpenAI API.

    Parameters:
    - role (str): The role of the message, must be either "system", "user", or "assistant".
    - content (str): The content of the message.

    Returns:
    - dict: A dictionary representation of the chat message.

    Raises:
    - ValueError: If the provided role is not one of "system", "user", or "assistant".
    """

    valid_roles = {"system", "user", "assistant"}
    if role not in valid_roles:
        raise ValueError("Invalid role, must be one of {valid_roles}.")
    return {"role": role, "content": content}


def request_chat_completion(
    messages: dict, model: str = "gpt-3.5-turbo", max_retries: int = 3, **kwargs: Any
) -> dict:
    """
    Requests a completion from OpenAI's Chat API.

    Parameters:
    - messages (dict): The messages sent to the API.
    - model (str, optional): The model to be used for the API call. Defaults to "gpt-3.5-turbo".
    - max_retries (int, optional): Maximum number of retries in case of API failures. Defaults to 3.
    - **kwargs: Additional keyword arguments passed to the openai.ChatCompletion.create method.

    Returns:
    - dict: The API response.

    Raises:
    - ChatAPIRequestException: For errors during the API request process.
    """

    last_error_msg = ""
    retry_delay = 1  # Initial delay for exponential backoff

    for attempt in range(max_retries):
        try:
            completion = openai.chat.completions.create(
                model=model, messages=messages, **kwargs
            )
            return completion
        except Exception as e:
            last_error_msg = str(e)
            logging.error("Attempt %d failed: %s", attempt + 1, last_error_msg)
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff

    raise ChatAPIRequestException(
        f"Failed after {max_retries} retries. Last error message: {last_error_msg}"
    )


def get_chat_response(
    prompt: str, sys_message: str = "", model: str = "gpt-3.5-turbo", **kwargs: Any
) -> str:
    """
    Generates a chat response using OpenAI's Chat API.

    Args:
        prompt (str): The message from the user.
        sys_message (str, optional): A system message for the LLM. Defaults to an empty string.
        model (str, optional): The name of the OpenAI model to use. Defaults to "gpt-3.5-turbo".
        **kwargs: Additional keyword arguments to pass to the `request_chat_completion` function.

    Returns:
        str: The content of the LLM's response.

    Raises:
        ChatAPIResponseException: For errors during the response processing.
    """

    messages = []
    if sys_message:
        messages.append(construct_chat_message("system", sys_message))

    messages.append(construct_chat_message("user", prompt))

    try:
        completion = request_chat_completion(messages, model=model, **kwargs)

        logging.info(
            "Successfully completed Chat API request. Total token usage: %d",
            completion.usage.total_tokens,
        )
        return completion.choices[0].message.content
    except ChatAPIRequestException as e:
        logging.error("Failed to retrieve completion from OpenAI Chat API: %s", e)
        raise ChatAPIResponseException("Error in processing Chat API request.") from e
