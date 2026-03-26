"""Tests for form sections."""
from dash import html
from dash_fn_form import FnForm


def test_sections_creates_fieldsets():
    def fn(a: float = 1.0, b: float = 2.0, c: str = "x"):
        pass

    form = FnForm(
        "_t_sections",
        fn,
        _sections=[("Numbers", ["a", "b"]), ("Text", ["c"])],
    )
    json_str = str(form.to_plotly_json())
    assert "Numbers" in json_str
    assert "Text" in json_str
    assert "Fieldset" in json_str


def test_sections_ungrouped_fields_appended():
    def fn(a: float = 1.0, b: float = 2.0, c: str = "x"):
        pass

    form = FnForm(
        "_t_sections_ungrouped",
        fn,
        _sections=[("Numbers", ["a"])],
    )
    # b and c should still appear (ungrouped)
    json_str = str(form.to_plotly_json())
    assert "Numbers" in json_str


def test_no_sections_flat_layout():
    def fn(a: float = 1.0, b: float = 2.0):
        pass

    form = FnForm("_t_no_sections", fn)
    json_str = str(form.to_plotly_json())
    assert "Fieldset" not in json_str
