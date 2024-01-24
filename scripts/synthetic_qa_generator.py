"""Script for Automated Generation of Synthetic Q&A Datasets."""

import argparse
import os
import logging
import pandas as pd
from tqdm import tqdm

from genaipy.extractors.pdf import extract_pages_text
from genaipy.openai_apis.chat import get_chat_response
from genaipy.prompts.build_prompt import build_prompt
from genaipy.prompts.generate_qa import GENERATE_QA_TPL
from genaipy.utilities import (
    convert_json_to_df,
    convert_df_to_messages,
    write_data_to_jsonl,
    validate_api_key,
)

# Logger configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Authentification
OPENAI_API_KEY = validate_api_key(env_var_name="OPENAI_API_KEY")

# CLI arguments
parser = argparse.ArgumentParser(description="Generate Synthetic Q&A Datasets.")
parser.add_argument(
    "--pdf_name", type=str, required=True, help="Name of the PDF document."
)
parser.add_argument("--start_page", type=int, required=True, help="Start page number.")
parser.add_argument("--end_page", type=int, required=True, help="End page number.")
parser.add_argument(
    "--output_path",
    type=str,
    default="../data/output/synthetic_dataset.jsonl",
    help="Output path for the dataset.",
)
args = parser.parse_args()

# Global variables
BASE_FOLDER = "../data/input"
SYS_MESSAGE_GEN = "You are a legal expert in AI law. You outline complex regulations and legal requirements with great detail and accuracy in simple English."
SYS_MESSAGE_DATA = "You are a legal expert in AI law and your job is to answer questions about the 'EU AI Act' by the European Union."
NUM_PAIRS = 3


# Functions
def validate_pdf_path(pdf_name):
    """Validates the existence of a PDF file."""
    full_path = os.path.join(BASE_FOLDER, pdf_name)
    full_path = os.path.normpath(full_path)

    if os.path.isfile(full_path):
        logging.info("PDF file located at path: %s", full_path)
    else:
        logging.error("PDF file not found at path: %s", full_path)
        raise FileNotFoundError(f"PDF file not found at path: {full_path}")

    return full_path


def extract_text(pdf_name, start_page, end_page):
    """Extracts text from a PDF document."""
    try:
        full_path = validate_pdf_path(pdf_name)
        pages = extract_pages_text(
            pdf_path=full_path, start_page=start_page, end_page=end_page
        )
        logging.info("Text loaded from %d pages.", len(pages))
        return pages
    except Exception as e:
        logging.error("Error in text extraction: %s", e)
        raise


def generate_qa_pairs(pages):
    """Generates Q&A pairs from text."""
    qa_dataset = []
    for page in tqdm(pages, desc="Generating Q&A pairs"):
        try:
            qa_prompt = build_prompt(
                template=GENERATE_QA_TPL, num=NUM_PAIRS, text=pages[page]["content"]
            )
            qa_response = get_chat_response(
                prompt=qa_prompt,
                sys_message=SYS_MESSAGE_GEN,
                model="gpt-4-1106-preview",
                response_format={"type": "json_object"},
            )
            qa_df = convert_json_to_df(qa_response)
            qa_dataset.append(qa_df)
            logging.info("Q&A pairs created for page #%d", page)
        except Exception as e:
            logging.error("Error in Q&A generation: %s", e)
            raise
    return qa_dataset


def compile_dataset(qa_dataset, output_path):
    """Compiles and saves the Q&A dataset."""
    try:
        final_df = pd.concat(qa_dataset, ignore_index=True)
        messages = convert_df_to_messages(
            df=final_df,
            system_msg=SYS_MESSAGE_DATA,
            user_col="question",
            assistant_col="answer",
        )
        write_data_to_jsonl(data=messages, file_path=output_path)
        logging.info("Dataset saved to %s", output_path)
    except Exception as e:
        logging.error("Error in dataset compilation: %s", e)
        raise


def main():
    """Main function of synthetic data generator"""
    try:
        pages = extract_text(args.pdf_name, args.start_page, args.end_page)
        qa_dataset = generate_qa_pairs(pages)
        compile_dataset(qa_dataset, args.output_path)
    except Exception as e:
        logging.error("Error in main function: %s", e)


if __name__ == "__main__":
    main()
