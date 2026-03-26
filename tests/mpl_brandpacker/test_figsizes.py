"""Tests for mpl_brandpacker.figsizes."""

import pytest

from mpl_brandpacker.figsizes import FigsizesBase, MM_TO_INCH


class TestFigsizesBase:
    def test_valid_tuple(self):
        class S(FigsizesBase):
            half = (3.46, 2.99)
            full = (6.93, 5.14)

        assert S.half == (3.46, 2.99)

    def test_rejects_scalar(self):
        with pytest.raises(ValueError, match="must be a .* tuple"):
            class S(FigsizesBase):
                bad = 42

    def test_rejects_three_tuple(self):
        with pytest.raises(ValueError, match="must be a .* tuple"):
            class S(FigsizesBase):
                bad = (1, 2, 3)

    def test_rejects_string_tuple(self):
        with pytest.raises(ValueError, match="must be a .* tuple"):
            class S(FigsizesBase):
                bad = ("a", "b")

    def test_is_tuple(self):
        class S(FigsizesBase):
            x = (4.0, 3.0)

        assert isinstance(S.x, tuple)
        w, h = S.x
        assert w == 4.0

    def test_mm_to_inch(self):
        class S(FigsizesBase):
            a4_width = (210 * MM_TO_INCH, 297 * MM_TO_INCH)

        w, h = S.a4_width
        assert abs(w - 8.27) < 0.01

    def test_dict_access(self):
        class S(FigsizesBase):
            half = (3.0, 2.0)

        assert S["half"] == (3.0, 2.0)
