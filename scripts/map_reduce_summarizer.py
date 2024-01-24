"""Script for generating summaries from PDFs with map-reduce technique."""

import os
import logging
from tqdm import tqdm

from genaipy.extractors.pdf import extract_pages_text
from genaipy.openai_apis.chat import get_chat_response
from genaipy.prompts.build_prompt import build_prompt
from genaipy.prompts.generate_summaries import (
    DEFAULT_SYS_MESSAGE,
    SUMMARY_PROMPT_TPL,
    REDUCE_SUMMARY_PROMPT_TPL,
)
from genaipy.utilities import write_string_to_txt, validate_api_key


# LOGGER CONFIG
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# AUTHENTIFICATION
OPENAI_API_KEY = validate_api_key(env_var_name="OPENAI_API_KEY")


# PARAMETERS
BASE_FOLDER = "../data/input"
OUTPUT_PATH = "../data/output/map_reduce_output.txt"

MAP_LLM = "gpt-3.5-turbo"
REDUCE_LLM = "gpt-4-1106-preview"
MAP_MAX_WORDS = 150
REDUCE_MAX_WORDS = 350


# FUNCTIONS
def validate_pdf_path(pdf_name):
    """Validates the existence of a PDF file at the given path."""
    full_path = os.path.join(BASE_FOLDER, pdf_name)
    full_path = os.path.normpath(
        full_path
    )  # normalize path for cross-platform compatability

    if os.path.isfile(full_path):
        logging.info("PDF file successfully located at path: %s", full_path)
    else:
        logging.error("PDF file not found at path: %s", full_path)
        raise FileNotFoundError(f"PDF file not found at path: {full_path}")

    return full_path


def process_pdf(full_path, start_page, end_page):
    """Extracts text from specified page range of a PDF file."""
    try:
        pages = extract_pages_text(
            pdf_path=full_path, start_page=start_page, end_page=end_page
        )
        logging.info("Successfully loaded text from %d PDF pages.", len(pages))
        return pages
    except Exception as e:
        logging.error("An error occured while processing PDF: %s", e)
        raise


def generate_map_summaries(pages):
    """Generates summaries for each page."""
    map_summaries = []
    for page in tqdm(pages, desc="Generating Map Summaries"):
        try:
            map_prompt = build_prompt(
                template=SUMMARY_PROMPT_TPL,
                text=pages[page]["content"],
                max_words=MAP_MAX_WORDS,
            )
            summary = get_chat_response(
                map_prompt, sys_message=DEFAULT_SYS_MESSAGE, model=MAP_LLM
            )
            map_summaries.append(summary)
            logging.info("Map Summary #%d: %s", page, summary)
        except Exception as e:
            logging.error("An error occured while generating summary #%d: %s", page, e)
            raise
    return map_summaries


def generate_reduce_summary(map_summaries):
    """Generates a final summary from map summaries using reduce summarization."""
    text = "\n".join(map_summaries).replace("\n\n", "")
    try:
        reduce_prompt = build_prompt(
            template=REDUCE_SUMMARY_PROMPT_TPL, text=text, max_words=REDUCE_MAX_WORDS
        )
        final_summary = get_chat_response(
            prompt=reduce_prompt,
            sys_message=DEFAULT_SYS_MESSAGE,
            model=REDUCE_LLM,
            max_tokens=1024,
        )
        logging.info("Final Reduce Summary:\n%s", final_summary)
        return final_summary
    except Exception as e:
        logging.error("An error occured while generating final summary: %s", e)
        raise


def save_summary(summary, output_path):
    """Saves the summary to a text file."""
    success = write_string_to_txt(text=summary.strip(), file_path=output_path)
    if success:
        logging.info("Summary successfully saved to %s", output_path)
    else:
        logging.error("Failed to save summary to %s", output_path)


def main():
    """Main function of the map-reduce summarizer."""
    pdf_name = input("Enter the name of the PDF file: ")
    start_page = input("Enter the start page number: ")
    end_page = input("Enter the end page number: ")

    try:
        start_page = int(start_page)
        end_page = int(end_page)
        full_path = validate_pdf_path(pdf_name)
        pages = process_pdf(full_path, start_page, end_page)
        map_summaries = generate_map_summaries(pages)
        final_summary = generate_reduce_summary(map_summaries)
        save_summary(final_summary, OUTPUT_PATH)
    except Exception as e:
        logging.error("An error occurred in the main function: %s", e)


# MAIN
if __name__ == "__main__":
    main()
