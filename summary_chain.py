"""Script for summary with blog post chain"""
import logging

from openai_apis.chat import get_chat_response
from prompts.summary_prompt import build_summary_prompt
from prompts.style_text_prompt import build_style_text_prompt
from prompts.generate_post_prompt import build_generate_post_prompt
from outlines.basic_summary_outline import BASIC_SUMMARY_OUTLINE


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
ARTICLE = "hello world"


# Define functions
def summarize_article(raw_text, max_summary_words=150):
    """Generates summary of article."""
    prompt = build_summary_prompt(text=raw_text, max_words=max_summary_words)
    summary = get_chat_response(prompt=prompt, temperature=0.2)
    return summary


def style_summary(summary_text, outline=BASIC_SUMMARY_OUTLINE):
    """Styles summary according to outline."""
    style_prompt = build_style_text_prompt(text=summary_text, tpl=outline.strip())
    styled_summary = get_chat_response(prompt=style_prompt, temperature=0)
    return styled_summary


def generate_post(styled_summary, max_post_words=100):
    """Generates post from styled summary."""
    generate_prompt = build_generate_post_prompt(
        text=styled_summary, max_words=max_post_words
    )
    post = get_chat_response(prompt=generate_prompt, temperature=0.5, model="gpt-4")
    return post


def main(raw_text):
    """Main function as entry point"""
    responses = []
    try:
        summary = summarize_article(raw_text)
        logging.info("Summary generated successfully:\n %s", summary)
        responses.append(summary)

        styled_summary = style_summary(summary)
        logging.info("Style applied to summary successfully:\n %s", styled_summary)
        responses.append(styled_summary)

        post = generate_post(styled_summary)
        logging.info("Post generated successfully:\n %s", post)

        return responses
    except Exception as e:
        logging.error("An error occurred: %s", e)
        raise


if __name__ == "__main__":
    # Run the main function and print the result
    result_post = main(ARTICLE)
    print(result_post)
