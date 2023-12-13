"""Module for social media post prompt templates and system messages."""

GENERATE_POST_TPL = """
Text sample:
```{text}```

Instructions:
Your task is to generate an engaging post about the provided text sample delimited by triple back ticks.

Guidelines:
- Clearly structure the post by using headings, paragraphs, and bulleted lists. 
- Write the post in first person.
- Limit your post to at most {max_words} words.

 Only return the engaging post in your response and nothing else.
"""
