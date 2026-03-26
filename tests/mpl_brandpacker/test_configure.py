"""Tests for mpl_brandpacker.configure."""

import warnings

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

import mpl_brandpacker
from mpl_brandpacker._config import _make_fig, _make_ax, is_configured
from mpl_brandpacker.axes import BrandAxes
from mpl_brandpacker.figure import BrandFigure


class _MyFig(BrandFigure):
    _brand_methods = ["set_title"]

    def set_title(self, title):
        self._test_title = title


class _MyAx(BrandAxes):
    _brand_methods = ["set_xlabel"]

    def set_xlabel(self, label):
        self._test_label = label


class TestConfigure:
    def test_basic(self):
        mpl_brandpacker.configure(figure_cls=_MyFig, axes_cls=_MyAx)
        assert is_configured()

    def test_with_style_fn(self):
        styled = []
        mpl_brandpacker.configure(
            figure_cls=_MyFig,
            axes_cls=_MyAx,
            style_fn=lambda ax, **kw: styled.append(True),
        )
        assert is_configured()

    def test_double_configure_warns(self):
        mpl_brandpacker.configure(figure_cls=_MyFig, axes_cls=_MyAx)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            mpl_brandpacker.configure(figure_cls=_MyFig, axes_cls=_MyAx)
            assert len(w) == 1
            assert "overwriting" in str(w[0].message)

    def test_validates_brand_methods(self):
        class BadFig(BrandFigure):
            _brand_methods = ["nonexistent"]

        with pytest.raises(ValueError, match="nonexistent.*not defined"):
            mpl_brandpacker.configure(figure_cls=BadFig)

    def test_validates_axes_brand_methods(self):
        class BadAx(BrandAxes):
            _brand_methods = ["nonexistent"]

        with pytest.raises(ValueError, match="nonexistent.*not defined"):
            mpl_brandpacker.configure(axes_cls=BadAx)

    def test_auto_wires_make_ax_on_figure(self):
        mpl_brandpacker.configure(figure_cls=_MyFig, axes_cls=_MyAx)

        fig = plt.figure()
        from mpl_brandpacker._config import get_make_fig
        get_make_fig()(fig)

        ax = fig.add_subplot(111)
        assert hasattr(ax, "_is_branded")
        plt.close(fig)


class TestPyplotIntegration:
    def test_subplots_patches_both(self):
        mpl_brandpacker.configure(figure_cls=_MyFig, axes_cls=_MyAx)
        import mpl_brandpacker.pyplot as bplt

        fig, ax = bplt.subplots()
        fig.set_title("test")
        ax.set_xlabel("x")
        assert fig._test_title == "test"
        assert ax._test_label == "x"
        bplt.close("all")

    def test_2x2_subplots(self):
        mpl_brandpacker.configure(figure_cls=_MyFig, axes_cls=_MyAx)
        import mpl_brandpacker.pyplot as bplt

        fig, axes = bplt.subplots(2, 2)
        assert all(hasattr(a, "_is_branded") for row in axes for a in row)
        bplt.close("all")

    def test_gcf_patches(self):
        mpl_brandpacker.configure(figure_cls=_MyFig, axes_cls=_MyAx)
        import mpl_brandpacker.pyplot as bplt

        bplt.figure()
        fig = bplt.gcf()
        assert hasattr(fig, "_is_branded")
        bplt.close("all")
