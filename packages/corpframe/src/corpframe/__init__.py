# Copyright (c) Simon Niederberger.
# Distributed under the terms of the MIT License.

"""corpframe — corporate design frame for charts and images."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("corpframe")
except PackageNotFoundError:
    __version__ = "unknown"

from corpframe.frame import apply_frame

__all__ = ["apply_frame"]
