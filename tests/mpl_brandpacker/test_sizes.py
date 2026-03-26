"""Tests for mpl_brandpacker.sizes — SizesBase and scaled()."""

from mpl_brandpacker.sizes import SizesBase


class TestSizesBase:
    def test_basic_values(self):
        class F(SizesBase):
            title = 10
            body = 8

        assert F.title == 10
        assert F.body == 8

    def test_scalers_declarative(self):
        class F(SizesBase):
            title = 10
            _scalers = {"big": 2.0}

        assert F._scalers["big"] == 2.0

    def test_add_scaler_runtime(self):
        class F(SizesBase):
            title = 10

        F.add_scaler("big", 2.0)
        assert F._scalers["big"] == 2.0

    def test_scaled_by_name(self):
        class F(SizesBase):
            title = 10
            body = 8
            _scalers = {"big": 2.0}

        with F.scaled("big"):
            assert F.title == 20.0
            assert F.body == 16.0

    def test_scaled_by_number(self):
        class F(SizesBase):
            title = 10

        with F.scaled(3.0):
            assert F.title == 30.0

    def test_restores_after_context(self):
        class F(SizesBase):
            title = 10
            _scalers = {"big": 2.0}

        with F.scaled("big"):
            pass
        assert F.title == 10

    def test_unknown_name_no_change(self):
        class F(SizesBase):
            title = 10

        with F.scaled("unknown"):
            assert F.title == 10

    def test_restores_on_exception(self):
        class F(SizesBase):
            title = 10
            _scalers = {"big": 3.0}

        try:
            with F.scaled("big"):
                assert F.title == 30.0
                raise ValueError("boom")
        except ValueError:
            pass
        assert F.title == 10

    def test_subclass_isolation(self):
        class A(SizesBase):
            title = 12
            _scalers = {"big": 2.0}

        class B(SizesBase):
            title = 8

        with A.scaled("big"):
            assert A.title == 24
            assert B.title == 8

    def test_selective_scaling(self):
        class F(SizesBase):
            title = 10
            body = 8
            footer = 6.5
            _scalers = {
                "presentation": (2.0, ["title", "body"]),
            }

        with F.scaled("presentation"):
            assert F.title == 20.0
            assert F.body == 16.0
            assert F.footer == 6.5  # unchanged

    def test_selective_restores(self):
        class F(SizesBase):
            title = 10
            footer = 6.5
            _scalers = {"x": (3.0, ["title"])}

        with F.scaled("x"):
            pass
        assert F.title == 10
        assert F.footer == 6.5

    def test_add_scaler_with_attrs(self):
        class F(SizesBase):
            title = 10
            body = 8

        F.add_scaler("big", 2.0, attrs=["title"])
        with F.scaled("big"):
            assert F.title == 20.0
            assert F.body == 8  # unchanged

    def test_scalers_not_shared_between_subclasses(self):
        class A(SizesBase):
            title = 10
            _scalers = {"x": 2.0}

        class B(SizesBase):
            title = 10

        assert "x" in A._scalers
        assert "x" not in B._scalers
