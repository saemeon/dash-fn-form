"""Tests for extended visibility operators."""
from dash_fn_form._forms import _check_visible


def test_gt_true():
    assert _check_visible(5, ">", 3) is True

def test_gt_false():
    assert _check_visible(2, ">", 3) is False

def test_gte_equal():
    assert _check_visible(3, ">=", 3) is True

def test_lt_true():
    assert _check_visible(2, "<", 3) is True

def test_lt_false():
    assert _check_visible(5, "<", 3) is False

def test_lte_equal():
    assert _check_visible(3, "<=", 3) is True

def test_gt_none_value():
    assert _check_visible(None, ">", 3) is False

def test_existing_eq_still_works():
    assert _check_visible("a", "==", "a") is True

def test_existing_in_still_works():
    assert _check_visible("a", "in", ["a", "b"]) is True
