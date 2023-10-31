"""Module for interfacing with the OpenAI Chat API"""

import logging
from time import sleep
from typing import Optional, Any
import openai


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

    if role not in ("system", "user", "assistant"):
        raise ValueError("Invalid role, must be 'system', 'user' or 'assistant'.")
    return {"role": role, "content": content}


def request_chat_completion(
    messages: dict, model: str = "gpt-3.5-turbo", max_retries: int = 3, **kwargs: Any
) -> Optional[dict]:
    """
    Requests a completion from OpenAI's Chat API.

    Parameters:
    - messages (dict): The messages sent to the API.
    - model (str, optional): The model to be used for the API call. Defaults to "gpt-3.5-turbo".
    - max_retries (int, optional): Maximum number of retries in case of API failures. Defaults to 3.
    - **kwargs: Additional keyword arguments passed to the openai.ChatCompletion.create method.

    Returns:
    - Optional[dict]: The API response if successful, 'None' otherwise.
    """

    last_error_msg = ""
    for _ in range(max_retries):
        try:
            completion = openai.ChatCompletion.create(
                model=model, messages=messages, **kwargs
            )
            return completion
        except Exception as e:
            last_error_msg = str(e)
            sleep(3)

    logging.error(
        "Failed after %s retries. Last error message: %s", max_retries, last_error_msg
    )
    return None


def get_chat_response(
    prompt: str, sys_message: str = "", model: str = "gpt-3.5-turbo", **kwargs: Any
) -> str:
    """
    Generates a chatbot response using OpenAI's Chat API.

    Args:
        prompt (str): The message from the user.
        sys_message (str, optional): A system message for the LLM. Defaults to an empty string.
        model (str, optional): The name of the OpenAI model to use. Defaults to "gpt-3.5-turbo".
        **kwargs: Additional keyword arguments to pass to the `request_chat_completion` function.

    Returns:
        Optional[str]: The content of the LLM's response or None if an error occurs.

    Raises:
        TypeError: Raised when `request_chat_completion` returns `None`.
    """
    messages = []
    if sys_message:
        messages.append(construct_chat_message("system", sys_message))

    messages.append(construct_chat_message("user", prompt))
    completion = request_chat_completion(messages, model=model, **kwargs)

    try:
        logging.info("Token usage: %s", completion["usage"])
        return completion.choices[0].message["content"]
    except TypeError as e:
        logging.error("Failed to retrieve completion from OpenAI Chat API: %s", {e})
        raise
