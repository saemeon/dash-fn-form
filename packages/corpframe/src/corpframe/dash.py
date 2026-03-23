# Copyright (c) Simon Niederberger.
# Distributed under the terms of the MIT License.

"""Dash integration for corpframe — one-click corporate chart capture.

Requires ``pip install corpframe[dash]`` (adds dash-capture, dash, plotly).

Usage::

    from corpframe.dash import corporate_capture_graph, corporate_renderer
"""

from __future__ import annotations

from typing import Any

try:
    from dash import dcc, html
    from dash_capture import capture_graph, plotly_strategy
except ImportError as e:
    raise ImportError(
        "corpframe.dash requires dash-capture and dash. "
        "Install with: pip install corpframe[dash]"
    ) from e

from corpframe.frame import apply_frame


def corporate_renderer(
    _target,
    _snapshot_img,
    title: str = "",
    subtitle: str = "",
    footnotes: str = "",
    sources: str = "",
):
    """Renderer that wraps captured image with corporate header and footer.

    Compatible with dash-capture's renderer protocol:
    ``(_target, _snapshot_img, **fields) -> None``.
    """
    framed = apply_frame(
        _snapshot_img(), title=title, subtitle=subtitle,
        footnotes=footnotes, sources=sources,
    )
    _target.write(framed)


def corporate_capture_graph(
    graph: str | dcc.Graph,
    trigger: str | Any = "Export (Corporate)",
    title: str = "",
    subtitle: str = "",
    footnotes: str = "",
    sources: str = "",
    strip_title: bool = True,
    strip_legend: bool = False,
    strip_annotations: bool = False,
    strip_margin: bool = False,
    filename: str = "chart_corporate.png",
    styles: dict | None = None,
    class_names: dict | None = None,
    field_components: Any = "dcc",
) -> html.Div:
    """One-click corporate capture button for a ``dcc.Graph``.

    Combines ``capture_graph`` with the corporate frame renderer.
    The wizard shows fields for title, subtitle, footnotes, and sources
    — pre-filled with the values passed here.
    """
    from dash_fn_forms import Field

    field_specs = {}
    if title:
        field_specs["title"] = Field(default=title, persist=True)
    if subtitle:
        field_specs["subtitle"] = Field(default=subtitle, persist=True)
    if footnotes:
        field_specs["footnotes"] = Field(default=footnotes, persist=True)
    if sources:
        field_specs["sources"] = Field(default=sources, persist=True)

    return capture_graph(
        graph,
        renderer=corporate_renderer,
        trigger=trigger,
        strip_title=strip_title,
        strip_legend=strip_legend,
        strip_annotations=strip_annotations,
        strip_margin=strip_margin,
        filename=filename,
        autogenerate=False,
        persist=True,
        styles=styles,
        class_names=class_names,
        field_specs=field_specs or None,
        field_components=field_components,
    )
