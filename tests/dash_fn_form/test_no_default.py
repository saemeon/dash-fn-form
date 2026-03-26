"""Tests for parameters with no default value."""

from dash_fn_form import FnForm


def test_int_no_default():
    def fn(x: int):
        pass

    form = FnForm("_t_int_nodef", fn)
    kw = form.build_kwargs([5])
    assert kw == {"x": 5}


def test_float_no_default():
    def fn(x: float):
        pass

    form = FnForm("_t_float_nodef", fn)
    kw = form.build_kwargs([3.14])
    assert kw == {"x": 3.14}


def test_str_no_default():
    def fn(name: str):
        pass

    form = FnForm("_t_str_nodef", fn)
    kw = form.build_kwargs(["Alice"])
    assert kw == {"name": "Alice"}


def test_bool_no_default():
    def fn(flag: bool):
        pass

    form = FnForm("_t_bool_nodef", fn)
    kw = form.build_kwargs([[]])
    assert kw == {"flag": False}


def test_mixed_default_and_no_default():
    def fn(x: int, y: float = 2.0):
        pass

    form = FnForm("_t_mixed_nodef", fn)
    kw = form.build_kwargs([10, 2.0])
    assert kw == {"x": 10, "y": 2.0}


def test_no_default_renders_component():
    def fn(x: int):
        pass

    form = FnForm("_t_nodef_render", fn)
    json_str = str(form.to_plotly_json())
    assert "Input" in json_str  # should render a number input
