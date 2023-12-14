"""Module with unit tests for prompt builder function."""

import logging
import pytest
from genaipy.prompts.build_prompt import build_prompt

# Configure logging to capture log messages for verification
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


# Unit tests
def test_simple_template():
    """Test with a simple template and matching keyword arguments"""
    result = build_prompt("Hello, {name}!", name="Alice")
    assert result == "Hello, Alice!"


def test_multiple_placeholders():
    """Test with multiple placeholders and matching keyword arguments"""
    result = build_prompt(
        "Coordinates: {latitude}, {longitude}",
        latitude="34.0522",
        longitude="-118.2437",
    )
    assert result == "Coordinates: 34.0522, -118.2437"


def test_no_placeholders():
    """Test with no placeholders and no keyword arguments"""
    result = build_prompt("No placeholders here")
    assert result == "No placeholders here"


def test_repeated_placeholders():
    """Test with repeated placeholders and matching keyword arguments"""
    result = build_prompt(
        "{greeting}, {name}! {greeting}!", greeting="Hello", name="Bob"
    )
    assert result == "Hello, Bob! Hello!"


def test_unused_keyword_arguments():
    """Test with additional unused keyword arguments"""
    result = build_prompt("Just a {word}", word="test", extra="unused")
    assert result == "Just a test"


def test_different_types():
    """Test with placeholders and keyword arguments of different types"""
    result = build_prompt("ID: {id}, Score: {score}", id=123, score=98.6)
    assert result == "ID: 123, Score: 98.6"


def test_missing_placeholder():
    """Test with a missing placeholder, expect a KeyError to be raised"""
    with pytest.raises(KeyError):
        build_prompt("Missing {missing_arg}")


def test_similar_but_not_matching():
    """Test with similar but not matching placeholder names, expect a KeyError"""
    with pytest.raises(KeyError) as exc_info:
        build_prompt("Hello, {Name}!", name="Eve")
    assert "Name" in str(exc_info.value)


def test_key_error_logging(caplog):
    """Test that a KeyError logs the correct error message"""
    with pytest.raises(KeyError):
        with caplog.at_level(logging.ERROR):
            build_prompt("Missing {missing_arg}")
    assert (
        "Missing required argument for placeholder 'missing_arg' in the template."
        in caplog.text
    )
