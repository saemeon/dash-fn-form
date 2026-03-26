"""Tests for mpl_brandpacker.colors."""

import pytest

from mpl_brandpacker.colors import ColorsBase


class TestColorsBase:
    def test_valid_hex(self):
        class C(ColorsBase):
            red = "#ff0000"
            blue = "#0000ff"

        assert C.red == "#ff0000"
        assert C.blue == "#0000ff"

    def test_rejects_named_color(self):
        with pytest.raises(ValueError, match="not a valid hex color"):
            class C(ColorsBase):
                bad = "red"

    def test_rejects_short_hex(self):
        with pytest.raises(ValueError, match="not a valid hex color"):
            class C(ColorsBase):
                bad = "#fff"

    def test_rejects_no_hash(self):
        with pytest.raises(ValueError, match="not a valid hex color"):
            class C(ColorsBase):
                bad = "ff0000"

    def test_is_str(self):
        class C(ColorsBase):
            x = "#aabbcc"

        assert isinstance(C.x, str)
        assert C.x == "#aabbcc"

    def test_printable_repr(self):
        class C(ColorsBase):
            """My colors."""
            a = "#111111"
            b = "#222222"

        r = repr(C)
        assert "a" in r
        assert "b" in r

    def test_dict_access(self):
        class C(ColorsBase):
            primary = "#123456"

        assert C["primary"] == "#123456"

    def test_dash_to_underscore(self):
        class C(ColorsBase):
            light_blue = "#aabbcc"

        assert C["light-blue"] == "#aabbcc"
