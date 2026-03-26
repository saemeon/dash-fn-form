"""Tests for read-only mode."""
from dash import html
from dash_fn_form import FnForm


def test_read_only_renders_spans():
    def fn(x: float = 3.14, name: str = "Alice"):
        pass

    form = FnForm("_t_readonly", fn, _read_only=True)
    json_str = str(form.to_plotly_json())
    assert "3.14" in json_str
    assert "Alice" in json_str


def test_read_only_bool_shows_yes_no():
    def fn(flag: bool = True):
        pass

    form = FnForm("_t_readonly_bool", fn, _read_only=True)
    json_str = str(form.to_plotly_json())
    assert "Yes" in json_str


def test_read_only_false_renders_inputs():
    def fn(x: float = 1.0):
        pass

    form = FnForm("_t_readonly_off", fn, _read_only=False)
    json_str = str(form.to_plotly_json())
    assert "Input" in json_str
