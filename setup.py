"""Setup file for genaipy lib"""

from setuptools import setup, find_packages

setup(
    name="genaipy",
    version="0.1.0",
    author="FraMaBu",
    description="A lightweight Python library for interacting and building applications with LLMs.",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4==4.12.2",
        "openai==1.3.6",
        "pypdf2==2.10.5",
        "requests==2.31.0",
        # Other dependencies
    ],
    python_requires=">=3.6",
)
