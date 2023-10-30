"""Module for interfacing with the OpenAI Chat API"""

from time import sleep
import openai


def construct_message_chat(role: str, content: str) -> dict:
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


def get_chat_completion(
    messages: dict, model: str = "gpt-3.5-turbo", max_retries: int = 3, **kwargs
) -> dict:
    """
    Retrieve a completion from OpenAI's Chat API.

    Parameters:
    - messages (dict): The messages sent to the API.
    - model (str, optional): The model to be used for the API call. Defaults to "gpt-3.5-turbo".
    - max_retries (int, optional): Maximum number of retries in case of API failures. Defaults to 3.
    - **kwargs: Additional keyword arguments passed to the openai.ChatCompletion.create method.

    Returns:
    - dict: The API response if successful. 'None' otherwise.
    """

    error_msg = ()
    for _ in range(max_retries):
        try:
            completion = openai.ChatCompletion.create(
                model=model, messages=messages, **kwargs
            )
            return completion
        except Exception as e:
            error_msg = str(e)
            sleep(3)
    print(f"Failed after {max_retries} retries. Last error message: {error_msg}")
    return None
