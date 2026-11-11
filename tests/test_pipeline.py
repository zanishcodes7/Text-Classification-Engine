import pytest
from engine.regex_tier import RegexClassifier
from engine.ml_tier import StatisticalMLClassifier

def test_regex_tier_complaint():
    engine = RegexClassifier()
    res = engine.classify("This is the worst service ever, cancel my account!")
    assert res is not None
    assert res["category"] == "Complaint"
    assert res["confidence"] == 1.0

def test_regex_tier_praise():
    engine = RegexClassifier()
    res = engine.classify("excellent")
    assert res is not None
    assert res["category"] == "Praise"
    assert res["confidence"] == 1.0

def test_ml_tier_fallback():
    engine = StatisticalMLClassifier()
    res = engine.classify("The screen turns blank upon opening reports")
    assert res["category"] in ["Complaint", "Praise", "Question"]
    assert "latency_ms" in res