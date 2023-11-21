"""Module for extracting content from PDF files."""

import logging
from typing import Dict, Optional, Union
import PyPDF2


def extract_pages_text(
    pdf_path: str, start_page: Optional[int] = None, end_page: Optional[int] = None
) -> Dict[int, Dict[str, Union[int, str]]]:
    """
    Extracts text from specified page range for given PDF file.

    Args:
        pdf_path (str): The path to the PDF file.
        start_page (int, optional): The starting page number.
            If not specified, defaults to the first page.
        end_page (int, optional): The ending page number.
            If not specified, defaults to the last page.

    Returns:
        Dict[int, Dict[str, Union[int, str]]]: A dictionary where each key is a sequential number
        starting from 1, and the values are dictionaries containing the 'page number' and 'content'.

    Raises:
        ValueError: If `start_page` is greater than `end_page`.
        IOError: If there is an error opening or accessing the PDF file.
    """
    pdf_pages = {}
    key_counter = 1

    if start_page is not None and end_page is not None and start_page > end_page:
        raise ValueError("start_page must not be greater than end_page.")

    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfFileReader(file)

            if start_page is None or start_page < 1:
                start_page = 1
            if end_page is None or end_page > reader.numPages:
                end_page = reader.numPages

            for page_num in range(start_page, end_page + 1):
                try:
                    page = reader.getPage(page_num - 1)
                    content = page.extractText()
                    pdf_pages[key_counter] = {
                        "page_number": page_num,
                        "content": content,
                    }
                    key_counter += 1
                except Exception as e:
                    logging.warning(
                        "Error extracting text from page %d: %s", page_num, e
                    )

    except IOError as e:
        logging.error("Error opening or accessing the file: %s", e)
        raise

    return pdf_pages
