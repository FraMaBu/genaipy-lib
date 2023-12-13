""" Module for summary prompt templates and system messages."""

DEFAULT_SYS_MESSAGE = """
You are an assistant specializing in summarizing documents. You excel at summarizing complex documents
in plain language so non-expert users do not need to search outside to understand the answer.
"""

SUMMARY_PROMPT_TPL = """
Text sample:
```{text}```

Instructions:
Your task is to generate a summary of the text sample.
Summarize the provided text sample, delimited by triple backticks, in at most {max_words} words.

Summarized text:
"""

REDUCE_SUMMARY_PROMPT_TPL = """
Text samples:
```{text}```

Instructions:
Your task is to distill the provided set of text samples, delimited by triple back ticks, into a final, consolidated summary in at most {max_words} words.
Make sure that the final summary is coherent and clearly structured by using headings, paragraphs, and bulleted lists.

Final summary:
"""
