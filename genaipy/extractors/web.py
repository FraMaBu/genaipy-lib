"""Module for extracting content from the web."""

import logging
import re
import requests
from bs4 import BeautifulSoup


def extract_tags_contents(url: str, tags: list) -> str:
    """
    Extracts and processes content from a webpage for given HTML tags.

    Args:
        url (str): The URL of the webpage to extract content from.
        tags (list): A list of HTML tags as strings to extract content from.

    Returns:
        str: A string containing the processed content extracted from the specified tags.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the web request.
        Exception: If there is an error in parsing the webpage.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        extracted_texts = []
        for element in soup.find_all(tags):
            text = " ".join(element.stripped_strings)
            text = re.sub(r"\W", " ", text)  # Replace special characters with space
            extracted_texts.append(text)

        return "\n\n".join(extracted_texts)

    except requests.exceptions.RequestException as e:
        logging.error("Error fetching the webpage: %s", e)
        raise

    # TODO: Consider implementing custom exception
    except Exception as e:  # Catch exceptions related to parsing
        logging.error("Error parsing the webpage: %s", e)
        raise
