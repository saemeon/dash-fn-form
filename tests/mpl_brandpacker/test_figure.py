"""Tests for mpl_brandpacker.figure."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from mpl_brandpacker.figure import BrandFigure, patch_figure


class TestBrandFigure:
    def test_brand_methods_default_empty(self):
        assert BrandFigure._brand_methods == []

    def test_subclass(self):
        class MyFig(BrandFigure):
            _brand_methods = ["set_title"]

            def set_title(self, title):
                self._test_title = title

        assert "set_title" in MyFig._brand_methods


class TestPatchFigure:
    def test_patches_methods(self):
        class MyFig(BrandFigure):
            _brand_methods = ["set_title"]

            def set_title(self, title):
                self._test_title = title

        fig = plt.figure()
        patch_figure(fig, MyFig)
        fig.set_title("hello")
        assert fig._test_title == "hello"
        plt.close(fig)

    def test_sets_marker(self):
        fig = plt.figure()
        patch_figure(fig, BrandFigure)
        assert hasattr(fig, "_is_branded")
        plt.close(fig)

    def test_creates_mpl_proxy(self):
        fig = plt.figure()
        patch_figure(fig, BrandFigure)
        assert hasattr(fig, "mpl")
        # proxy should access original Figure methods
        size = fig.mpl.get_size_inches()
        assert len(size) == 2
        plt.close(fig)

    def test_no_double_patch(self):
        call_count = 0

        class MyFig(BrandFigure):
            _brand_methods = ["set_title"]

            def set_title(self, title):
                nonlocal call_count
                call_count += 1

        fig = plt.figure()
        patch_figure(fig, MyFig)
        patch_figure(fig, MyFig)  # second call should be no-op
        fig.set_title("x")
        assert call_count == 1
        plt.close(fig)

    def test_extra_patches(self):
        class MyFig(BrandFigure):
            _brand_methods = ["set_title"]

            def set_title(self, title):
                self._test_title = title

        fig = plt.figure()
        patch_figure(fig, MyFig, extra_patches={"suptitle": "set_title"})
        fig.suptitle("redirected")
        assert fig._test_title == "redirected"
        plt.close(fig)


class TestAxesWrapping:
    def _setup(self):
        class MyFig(BrandFigure):
            _brand_methods = []

        def make_ax(ax, **kw):
            ax._test_patched = True
            return ax

        return MyFig, make_ax

    def test_subplots_auto_patches(self):
        MyFig, make_ax = self._setup()
        fig = plt.figure()
        patch_figure(fig, MyFig, make_ax=make_ax)
        axes = fig.subplots(2, 2)
        assert all(getattr(a, "_test_patched", False) for a in axes.flatten())
        plt.close(fig)

    def test_add_subplot_auto_patches(self):
        MyFig, make_ax = self._setup()
        fig = plt.figure()
        patch_figure(fig, MyFig, make_ax=make_ax)
        ax = fig.add_subplot(111)
        assert ax._test_patched
        plt.close(fig)

    def test_add_axes_auto_patches(self):
        MyFig, make_ax = self._setup()
        fig = plt.figure()
        patch_figure(fig, MyFig, make_ax=make_ax)
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        assert ax._test_patched
        plt.close(fig)

    def test_no_make_ax_no_wrapping(self):
        fig = plt.figure()
        patch_figure(fig, BrandFigure)  # no make_ax
        ax = fig.add_subplot(111)
        assert not hasattr(ax, "_test_patched")
        plt.close(fig)
