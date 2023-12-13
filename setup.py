"""Setup file for genaipy lib"""

from setuptools import setup

setup(
    name="genaipy",
    version="0.1.0",
    packages=["genaipy"],
    install_requires=[
        "beautifulsoup4==4.12.2",
        "openai==1.3.6",
        "pypdf2==2.10.5",
        # Other dependencies
    ],
)
