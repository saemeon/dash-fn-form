"""Tests for layout configurations (Accordion, Tabs, dmc backend)."""
from dash_fn_form import FnForm
from dash_fn_form.layout import Accordion, Section, Tabs


def test_accordion_html_layout():
    def fn(a: float = 1.0, b: float = 2.0, c: str = "x"):
        pass
    form = FnForm("_t_acc_html", fn, _layout=Accordion([
        Section("Numbers", ["a", "b"]),
        Section("Text", ["c"]),
    ]), _field_components="dcc")
    json_str = str(form.to_plotly_json())
    assert "Details" in json_str
    assert "Numbers" in json_str


def test_accordion_dmc_layout():
    def fn(a: float = 1.0, b: str = "x"):
        pass
    form = FnForm("_t_acc_dmc", fn, _layout=Accordion([
        Section("Group", ["a", "b"]),
    ]), _field_components="dmc")
    json_str = str(form.to_plotly_json())
    assert "Accordion" in json_str


def test_tabs_html_layout():
    def fn(a: float = 1.0, b: str = "x"):
        pass
    form = FnForm("_t_tabs_html", fn, _layout=Tabs([
        Section("Tab1", ["a"]),
        Section("Tab2", ["b"]),
    ]), _field_components="dcc")
    json_str = str(form.to_plotly_json())
    assert "Tab" in json_str


def test_tabs_dmc_layout():
    def fn(a: float = 1.0, b: str = "x"):
        pass
    form = FnForm("_t_tabs_dmc", fn, _layout=Tabs([
        Section("T1", ["a"]),
        Section("T2", ["b"]),
    ]), _field_components="dmc")
    json_str = str(form.to_plotly_json())
    assert "Tabs" in json_str


def test_sections_shorthand_with_dmc():
    def fn(a: float = 1.0, b: str = "x"):
        pass
    form = FnForm("_t_sec_dmc", fn, _sections=[
        ("Group", ["a", "b"]),
    ], _field_components="dmc")
    json_str = str(form.to_plotly_json())
    assert "Accordion" in json_str


def test_accordion_remaining_fields():
    def fn(a: float = 1.0, b: float = 2.0, extra: str = "y"):
        pass
    form = FnForm("_t_acc_remain", fn, _layout=Accordion([
        Section("Numbers", ["a", "b"]),
    ], remaining_fields="bottom"), _field_components="dcc")
    # extra should still appear
    json_str = str(form.to_plotly_json())
    assert "Extra" in json_str


def test_accordion_default_open():
    def fn(a: float = 1.0, b: str = "x"):
        pass
    form = FnForm("_t_acc_open", fn, _layout=Accordion([
        Section("Open", ["a"], default_open=True),
        Section("Closed", ["b"], default_open=False),
    ]), _field_components="dcc")
    json_str = str(form.to_plotly_json())
    assert "Open" in json_str
