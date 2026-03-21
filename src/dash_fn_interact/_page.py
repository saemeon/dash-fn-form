# Copyright (c) Simon Niederberger.
# Distributed under the terms of the MIT License.

"""Page — ordered collection of interact panels assembled into a Dash app."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any

from dash import Dash, html

from dash_fn_interact._interact import interact as _interact

_THIS_MODULES = {"dash_fn_interact._page", "dash_fn_interact.page"}


def _caller_name() -> str:
    """Walk the call stack to find the first frame outside this library."""
    for info in inspect.stack():
        mod = info.frame.f_globals.get("__name__", "")
        if mod and mod not in _THIS_MODULES:
            return mod
    return "__main__"


class Page:
    """Ordered collection of interact panels assembled into a Dash app.

    Build a multi-panel app by calling :meth:`interact` and :meth:`add` in
    order, then call :meth:`run` to launch — no manual ``app.layout`` wiring
    needed.

    Examples
    --------
    ::

        page = Page()

        page.add(html.H1("My App"))

        @page.interact
        def sine_wave(amplitude: float = 1.0, frequency: float = 2.0):
            ...

        page.add(html.Hr())

        @page.interact(amplitude=(0.0, 3.0, 0.1))
        def histogram(n_samples: int = 500, mean: float = 0.0):
            ...

        page.run(debug=True)
    """

    def __init__(self) -> None:
        self._divs: list[Any] = []

    # ------------------------------------------------------------------
    # Building blocks

    def interact(
        self,
        fn: Callable | None = None,
        *,
        _manual: bool = False,
        **kwargs: Any,
    ) -> html.Div | Callable:
        """Add an interact panel to the page.

        Identical signature to :func:`~dash_fn_interact.interact`.  Can be
        used as a direct call or as a decorator (with or without arguments).
        The resulting panel is appended to the page in call order.

        Parameters
        ----------
        fn :
            Callable whose signature drives the form.  When omitted a
            decorator is returned — useful for ``@page.interact(...)`` syntax.
        _manual :
            Add an *Apply* button instead of live updates.
        **kwargs :
            Per-field shorthands forwarded to :func:`~dash_fn_interact.interact`.
        """
        if fn is None:
            def decorator(f: Callable) -> html.Div:
                return self.interact(f, _manual=_manual, **kwargs)
            return decorator

        panel = _interact(fn, _manual=_manual, **kwargs)
        self._divs.append(panel)
        return panel

    def add(self, *components: Any) -> None:
        """Append arbitrary Dash components to the page.

        Use this for headings, dividers, descriptive text, or any layout
        element that does not come from a function form.

        Example::

            page.add(html.H2("Section title"), html.Hr())
        """
        self._divs.extend(components)

    # ------------------------------------------------------------------
    # Assembly

    def build_app(self, *, name: str | None = None) -> Dash:
        """Assemble and return a configured :class:`~dash.Dash` app.

        The app's ``layout`` is set to an ``html.Div`` containing all panels
        and components added so far, in insertion order.  All callbacks have
        already been registered by the individual :meth:`interact` calls.

        Parameters
        ----------
        name :
            Passed to ``Dash(name)``.  Defaults to the caller's ``__name__``
            (resolved via the call stack), which is correct for scripts run
            directly with ``python app.py``.
        """
        if name is None:
            name = _caller_name()
        app = Dash(name)
        app.layout = html.Div(
            self._divs,
            style={"fontFamily": "sans-serif", "padding": "32px", "maxWidth": "960px"},
        )
        return app

    def run(self, *, name: str | None = None, **kwargs: Any) -> None:
        """Build the app and start the Dash development server.

        Parameters
        ----------
        name :
            Forwarded to :meth:`build_app`.
        **kwargs :
            Forwarded to ``app.run()`` (e.g. ``debug=True``, ``port=8050``).
        """
        if name is None:
            name = _caller_name()
        self.build_app(name=name).run(**kwargs)
