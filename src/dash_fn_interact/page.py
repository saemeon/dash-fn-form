# Copyright (c) Simon Niederberger.
# Distributed under the terms of the MIT License.

"""Implicit (Streamlit-style) convenience layer over :class:`~dash_fn_interact.Page`.

Instead of constructing a :class:`~dash_fn_interact.Page` object explicitly,
import ``interact``, ``add``, and ``run`` from this module and call them at
module level.  A shared default :class:`~dash_fn_interact.Page` instance
accumulates the panels in call order.

Usage::

    from dash_fn_interact.page import interact, add, run
    from dash import html

    add(html.H1("My App"))

    @interact
    def sine_wave(amplitude: float = 1.0, frequency: float = 2.0):
        ...

    add(html.Hr())

    @interact
    def histogram(n_samples: int = 500, mean: float = 0.0):
        ...

    run(debug=True)

Notes
-----
The default page is a module-level singleton.  It is created once at import
time and accumulates all panels until ``run()`` is called.  This means the
module cannot be safely re-imported in the same process to start a fresh page
— use :class:`~dash_fn_interact.Page` directly if you need multiple pages or
want explicit control.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from dash_fn_interact._page import Page

_page = Page()


def interact(
    fn: Callable | None = None,
    *,
    _manual: bool = False,
    **kwargs: Any,
) -> Any:
    """Add an interact panel to the default page.

    See :meth:`~dash_fn_interact.Page.interact` for full documentation.
    """
    return _page.interact(fn, _manual=_manual, **kwargs)


def add(*components: Any) -> None:
    """Append arbitrary Dash components to the default page.

    See :meth:`~dash_fn_interact.Page.add` for full documentation.
    """
    _page.add(*components)


def run(**kwargs: Any) -> None:
    """Build and run the default page as a Dash app.

    See :meth:`~dash_fn_interact.Page.run` for full documentation.
    """
    _page.run(**kwargs)
