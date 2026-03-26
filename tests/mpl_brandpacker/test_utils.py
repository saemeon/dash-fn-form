"""Tests for mpl_brandpacker.utils."""

import matplotlib
matplotlib.use("Agg")

from mpl_brandpacker.utils import (
    PrintableEnum,
    get_text_bbox,
    separate_kwargs,
    available_kw,
    filter_kw,
)


class TestPrintableEnum:
    def test_basic(self):
        class E(PrintableEnum):
            """My enum."""
            a = 1
            b = 2

        assert E.a.value == 1
        assert "a" in repr(E)
        assert "b" in repr(E)

    def test_getitem_with_dash(self):
        class E(PrintableEnum):
            light_blue = "lb"

        assert E["light-blue"] == E.light_blue


class TestGetTextBbox:
    def test_none_returns_zero(self):
        box = get_text_bbox(None)
        assert box.width_inch == 0
        assert box.height_inch == 0

    def test_string_returns_nonzero(self):
        box = get_text_bbox("Hello", fontsize=12)
        assert box.width_inch > 0
        assert box.height_inch > 0

    def test_larger_text_wider(self):
        small = get_text_bbox("Hi")
        large = get_text_bbox("Hello World This Is Long")
        assert large.width_inch > small.width_inch


class TestSeparateKwargs:
    def test_basic(self):
        def fn_a(x, y):
            pass

        def fn_b(z):
            pass

        a_kw, b_kw, rest = separate_kwargs([fn_a, fn_b], x=1, y=2, z=3, w=4)
        assert a_kw == {"x": 1, "y": 2}
        assert b_kw == {"z": 3}
        assert rest == {"w": 4}

    def test_empty(self):
        def fn(x):
            pass

        (fn_kw, rest) = separate_kwargs([fn])
        assert fn_kw == {}
        assert rest == {}

    def test_all_consumed(self):
        def fn(a, b, c):
            pass

        fn_kw, rest = separate_kwargs([fn], a=1, b=2, c=3)
        assert fn_kw == {"a": 1, "b": 2, "c": 3}
        assert rest == {}


class TestAvailableKw:
    def test_basic(self):
        def fn(a, b, c=3):
            pass

        assert available_kw(fn) == ["a", "b", "c"]


class TestFilterKw:
    def test_basic(self):
        result = filter_kw(["a", "c"], a=1, b=2, c=3)
        assert result == {"a": 1, "c": 3}
