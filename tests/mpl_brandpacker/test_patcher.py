"""Tests for mpl_brandpacker.patcher."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from mpl_brandpacker.patcher import MethodProxy, patch_method


class TestPatchMethod:
    def test_binds_method(self):
        class Source:
            def greet(self):
                return f"hello from {type(self).__name__}"

        fig = plt.figure()
        patch_method(fig, Source, "greet")
        assert fig.greet() == "hello from Figure"
        plt.close(fig)

    def test_source_name_differs(self):
        class Source:
            def _internal(self):
                return "internal"

        fig = plt.figure()
        patch_method(fig, Source, "public", "_internal")
        assert fig.public() == "internal"
        plt.close(fig)

    def test_does_not_affect_other_instances(self):
        class Source:
            def custom(self):
                return "custom"

        fig1 = plt.figure()
        fig2 = plt.figure()
        patch_method(fig1, Source, "custom")
        assert hasattr(fig1, "custom")
        assert not hasattr(fig2, "custom")
        plt.close("all")


class TestMethodProxy:
    def test_forwards_to_original(self):
        fig = plt.figure()
        proxy = MethodProxy(fig, Figure)
        # proxy.get_size_inches should call Figure.get_size_inches(fig)
        size = proxy.get_size_inches()
        assert len(size) == 2
        plt.close(fig)

    def test_bypasses_patched_method(self):
        class Source:
            def custom_method(self):
                return "patched"

        fig = plt.figure()
        patch_method(fig, Source, "custom_method")
        assert fig.custom_method() == "patched"

        proxy = MethodProxy(fig, Figure)
        # proxy accesses original Figure, which has no custom_method
        # but has get_size_inches
        size = proxy.get_size_inches()
        assert len(size) == 2
        plt.close(fig)
