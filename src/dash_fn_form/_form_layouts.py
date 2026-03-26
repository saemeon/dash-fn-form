"""Layout rendering functions for form field grouping.

Internal module — rendering logic for sections, accordion, and tabs layouts.
Supports both plain HTML and Mantine (dmc) backends.
"""

from __future__ import annotations

from typing import Any


def _render_sections_html(sections, field_components, remaining="bottom"):
    """Render sections as html.Fieldset."""
    from dash import html

    children = []
    used = set()
    for name, fields in sections:
        items = [field_components[f] for f in fields if f in field_components]
        used.update(f for f in fields if f in field_components)
        if items:
            children.append(
                html.Fieldset(
                    [
                        html.Legend(
                            name,
                            style={
                                "fontWeight": "bold",
                                "fontSize": "0.9em",
                                "color": "#555",
                            },
                        )
                    ]
                    + items,
                    style={
                        "border": "1px solid #ddd",
                        "borderRadius": "4px",
                        "padding": "8px 12px",
                        "marginBottom": "12px",
                    },
                )
            )
    rest = [v for k, v in field_components.items() if k not in used]
    if rest and remaining == "top":
        return rest + children
    elif rest and remaining == "bottom":
        return children + rest
    return children


def _render_accordion_dmc(layout, field_components):
    """Render Accordion layout with dmc components."""
    import dash_mantine_components as dmc

    items = []
    used: set[str] = set()
    for section in layout.sections:
        fields = [field_components[f] for f in section.fields if f in field_components]
        used.update(f for f in section.fields if f in field_components)
        if fields:
            items.append(
                dmc.AccordionItem(
                    [dmc.AccordionControl(section.name), dmc.AccordionPanel(fields)],
                    value=section.name,
                )
            )
    open_values = [s.name for s in layout.sections if s.default_open]
    accordion = dmc.Accordion(
        items,
        value=open_values
        if layout.multiple
        else (open_values[0] if open_values else None),
        multiple=layout.multiple,
    )
    rest = [v for k, v in field_components.items() if k not in used]
    if rest and layout.remaining_fields == "top":
        return rest + [accordion]
    elif rest and layout.remaining_fields == "bottom":
        return [accordion] + rest
    return [accordion]


def _render_accordion_html(layout, field_components):
    """Render Accordion layout with html.Details/Summary."""
    from dash import html

    children = []
    used: set[str] = set()
    for section in layout.sections:
        fields = [field_components[f] for f in section.fields if f in field_components]
        used.update(f for f in section.fields if f in field_components)
        if fields:
            children.append(
                html.Details(
                    [
                        html.Summary(
                            section.name,
                            style={
                                "fontWeight": "bold",
                                "cursor": "pointer",
                                "marginBottom": "8px",
                            },
                        )
                    ]
                    + fields,
                    open=section.default_open,
                    style={"marginBottom": "12px", "padding": "4px"},
                )
            )
    rest = [v for k, v in field_components.items() if k not in used]
    if rest and layout.remaining_fields == "top":
        return rest + children
    elif rest and layout.remaining_fields == "bottom":
        return children + rest
    return children


def _render_tabs_dmc(layout, field_components):
    """Render Tabs layout with dmc components."""
    import dash_mantine_components as dmc

    used: set[str] = set()
    tab_buttons = []
    tab_panels = []
    first_value = None
    for section in layout.sections:
        fields = [field_components[f] for f in section.fields if f in field_components]
        used.update(f for f in section.fields if f in field_components)
        if fields:
            if first_value is None:
                first_value = section.name
            tab_buttons.append(dmc.TabsTab(section.name, value=section.name))
            tab_panels.append(dmc.TabsPanel(fields, value=section.name))
    tabs = dmc.Tabs(
        [dmc.TabsList(tab_buttons)] + tab_panels,
        value=first_value,
    )
    rest = [v for k, v in field_components.items() if k not in used]
    if rest and layout.remaining_fields == "top":
        return rest + [tabs]
    elif rest and layout.remaining_fields == "bottom":
        return [tabs] + rest
    return [tabs]


def _render_tabs_html(layout, field_components):
    """Render Tabs layout with dcc.Tabs."""
    from dash import dcc, html

    used: set[str] = set()
    tabs = []
    for section in layout.sections:
        fields = [field_components[f] for f in section.fields if f in field_components]
        used.update(f for f in section.fields if f in field_components)
        if fields:
            tabs.append(
                dcc.Tab(
                    label=section.name,
                    children=[html.Div(fields, style={"padding": "8px"})],
                )
            )
    result = [dcc.Tabs(tabs)]
    rest = [v for k, v in field_components.items() if k not in used]
    if rest and layout.remaining_fields == "top":
        return rest + result
    elif rest and layout.remaining_fields == "bottom":
        return result + rest
    return result


def render_layout(
    layout: Any,
    sections: list[tuple[str, list[str]]] | None,
    field_components: dict[str, Any],
    use_dmc: bool,
) -> list[Any]:
    """Dispatch to the appropriate layout renderer.

    Parameters
    ----------
    layout :
        An ``Accordion`` or ``Tabs`` layout object, or ``None``.
    sections :
        Tuple shorthand ``[(name, [fields]), ...]``, or ``None``.
    field_components :
        Dict mapping field names to their rendered Dash components.
    use_dmc :
        Whether to use Mantine components.
    """
    from dash_fn_form.layout import Accordion, Section, Tabs

    if layout is not None:
        if isinstance(layout, Accordion):
            return (
                _render_accordion_dmc(layout, field_components)
                if use_dmc
                else _render_accordion_html(layout, field_components)
            )
        if isinstance(layout, Tabs):
            return (
                _render_tabs_dmc(layout, field_components)
                if use_dmc
                else _render_tabs_html(layout, field_components)
            )
        return list(field_components.values())

    if sections is not None:
        if use_dmc:
            acc = Accordion([Section(name, fields) for name, fields in sections])
            return _render_accordion_dmc(acc, field_components)
        return _render_sections_html(sections, field_components)

    return list(field_components.values())
