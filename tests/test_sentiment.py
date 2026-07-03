"""Unit tests for app.sentiment — these run in the pipeline's test stage."""

import pytest

from app.sentiment import analyze


def test_positive_text():
    result = analyze("I love this, it is great and amazing")
    assert result["label"] == "positive"
    assert result["score"] > 0


def test_fabulous_text():
    result = analyze("This workshop is fabulous")
    assert result["label"] == "positive"
    assert result["score"] > 0


def test_fun_text():
    result = analyze("This workshop is fun")
    assert result["label"] == "positive"
    assert result["score"] > 0


def test_awesome_text():
    result = analyze("This workshop is awesome")
    assert result["label"] == "positive"
    assert result["score"] > 0


def test_cool_text():
    result = analyze("This workshop is cool")
    assert result["label"] == "positive"
    assert result["score"] > 0


def test_negative_text():
    result = analyze("This is terrible and awful, the worst")
    assert result["label"] == "negative"
    assert result["score"] < 0


def test_neutral_text():
    result = analyze("the item is on the table")
    assert result["label"] == "neutral"
    assert result["score"] == 0


def test_empty_text_raises():
    with pytest.raises(ValueError):
        analyze("   ")
