"""Tests for mpl_brandpacker.axes."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from mpl_brandpacker.axes import BrandAxes, patch_axes


class TestPatchAxes:
    def test_patches_methods(self):
        class MyAx(BrandAxes):
            _brand_methods = ["set_xlabel"]

            def set_xlabel(self, label, **kw):
                self._test_label = label

        fig, ax = plt.subplots()
        patch_axes(ax, MyAx)
        ax.set_xlabel("hello")
        assert ax._test_label == "hello"
        plt.close(fig)

    def test_sets_marker(self):
        fig, ax = plt.subplots()
        patch_axes(ax, BrandAxes)
        assert hasattr(ax, "_is_branded")
        plt.close(fig)

    def test_creates_mpl_proxy(self):
        fig, ax = plt.subplots()
        patch_axes(ax, BrandAxes)
        assert hasattr(ax, "mpl")
        # proxy calls original
        ax.mpl.set_xlabel("original")
        plt.close(fig)

    def test_no_double_patch(self):
        fig, ax = plt.subplots()
        patch_axes(ax, BrandAxes)
        patch_axes(ax, BrandAxes)  # no-op
        plt.close(fig)

    def test_style_fn_called(self):
        styled = []

        def my_style(ax, **kw):
            styled.append(True)

        fig, ax = plt.subplots()
        patch_axes(ax, BrandAxes, style_fn=my_style)
        assert len(styled) == 1
        plt.close(fig)

    def test_style_fn_receives_kwargs(self):
        received = {}

        def my_style(ax, color="red", **kw):
            received["color"] = color

        fig, ax = plt.subplots()
        patch_axes(ax, BrandAxes, style_fn=my_style, color="blue")
        assert received["color"] == "blue"
        plt.close(fig)

    def test_twinx_fn(self):
        twinx_called = []

        def my_twinx(ax):
            twinx_called.append(True)
            return ax

        fig, ax = plt.subplots()
        patch_axes(ax, BrandAxes, twinx_fn=my_twinx)
        ax.twinx()
        assert len(twinx_called) == 1
        plt.close(fig)

    def test_patch_legend_false(self):
        class MyAx(BrandAxes):
            _brand_methods = ["legend"]

            def legend(self, **kw):
                return "custom"

        fig, ax = plt.subplots()
        patch_axes(ax, MyAx, patch_legend=False)
        # legend should be the original, not MyAx.legend
        result = ax.legend()
        assert result != "custom"
        plt.close(fig)
