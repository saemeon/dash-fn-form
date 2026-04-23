# dash-fn-form

Introspection-based UI engine for Plotly Dash. Transforms a type-hinted Python function into a reactive form: inspect the signature → build controls → render the return value.

Import name: `dash_fn_form` (singular, aligned with `dash-pydantic-form`).

## Role in the brand-toolkit family

```
dash-fn-form → dash-interact (pyplot-style convenience layer)
            └→ dash-capture → corpframe[dash] (branded export)
```

- This package is the **form engine**. It knows nothing about pages or capture.
- `dash-interact` wraps this with a singleton `page` API (`@page.interact`, `page.columns()`, `page.sidebar()`, `page.tabs()`). Most users install dash-interact, not this directly.
- Keep this layer generic — no brand styling, no page-level concepts.

## Design philosophy

dash-fn-form (together with dash-interact) aims to be **the Dash equivalent of ipywidgets `interact`**: same three-level API (`interact` / `interactive` / `interactive_output`), same auto-widget-from-type-hints approach, same low-barrier entry.

Inspirations vendored under `dash-fn-form/dash-pydantic-form/` for reference, and under `dash-interact/ipywidgets/`, `dash-interact/py-shiny/` in the sibling package.

## Type → control mapping

| Python type | Control |
|---|---|
| `float` | Number input (slider with `(min, max, step)`) |
| `int` | Number input (integer step) |
| `bool` | Checkbox |
| `Literal[A, B, C]` | Dropdown |
| `str` | Text input |
| `date` / `datetime` | Date picker |
| `list[T]` / `tuple[T, ...]` | Comma-separated input |
| `T \| None` | Same as `T`, submits `None` when empty |
| `Path`, `Enum`, `list[Literal]`, etc. | 13+ hints supported in total |

## Layout system (form-level)

Three levels of complexity, all implemented:

### Level 0 — flat
```python
FnForm("id", fn)
```

### Level 1 — `_sections` shorthand (fieldsets)
```python
FnForm("id", fn, _sections=[
    ("Display", ["title", "color"]),
    ("Export", ["dpi", "format"]),
])
```
Renders as `html.Fieldset` + `html.Legend`. Zero deps.

### Level 2 — `_layout` objects
```python
from dash_fn_form.layout import Accordion, Tabs, Section

FnForm("id", fn, _layout=Accordion([
    Section("Display", ["title", "color"], default_open=True),
    Section("Export", ["dpi", "format"]),
]))
```

Layout types:
- `Accordion` — `html.Details`/`html.Summary` (no Mantine dep) + optional dmc backend
- `Tabs` — `dcc.Tabs`/`dcc.Tab`
- **No `Steps` layout** — decided against (architectural mismatch with flat-function model)

Config dataclasses live in [src/dash_fn_form/layout.py](src/dash_fn_form/layout.py):
- `Section(name, fields, default_open=True, description=None)`
- `Accordion(sections, remaining_fields="top", multiple=True)`
- `Tabs(sections, remaining_fields="top")`

Architectural note: build `field_components: dict[str, Component]` first, then lay out. This separates field construction from arrangement.

## Features implemented (as of 2026-03-26)

- `_sections`, `_layout` (Accordion/Tabs with dmc backend)
- `_read_only=True`
- Visibility operators: `==`, `!=`, `>`, `>=`, `<`, `<=`, `in`, `not in`
- No-default parameters (`def fn(x: int):` works)
- `_zero_default` + `required` flag
- `Field()` with validation, description, label, `col_span`, `visible`, `persist`
- Dirty field tracking (via `register_dirty_tracking()`)
- Cross-field validator (`FnForm(_validator=...)`)

## Open backlog

From `dash-interact/_notes.md` (dash-interact-level, but touches this package):
- **Table/ag-grid field** for DataFrame inputs — worth adopting from dash-pydantic-form
- **Clientside value gathering** — single JS callback collects all field values. Perf win for large forms
- **i18n** — en/fr translations for UI strings
- **Enter-to-submit in manual mode** — ipywidgets has this, we don't
- **DataPort** (dash-interact-level) — designed, not implemented

## dash-pydantic-form comparison

Vendored source at `dash-fn-form/dash-pydantic-form/` for reference.

**Adopted:** form sections/layout, read-only mode, extended visibility operators, dirty tracking.

**Still to adopt:** ag-grid/table field, clientside value gathering, i18n.

**Not adopting (architectural mismatch):** Steps layout, nested models, discriminated unions, lists of complex objects. dash-fn-form's flat-function model intentionally can't express these.

**Our advantages over dash-pydantic-form:**
- Zero-schema (just a function, no Pydantic model)
- Multi-component-library (dcc, dbc, dmc vs Mantine-only)
- Tuple shorthand for sliders
- Auto-rendering of return values (Figure, DataFrame, dict)
- No-default parameters
- Page API lives in dash-interact (pyplot-style singleton)

## ipywidgets comparison — feature parity

Done: auto-slider, tuple shorthand, `Literal` → dropdown, `fixed()`, `interact.options()`, three-level API, `interact_manual`.

Diverging: auto-slider heuristic (we keep min≥0 for positive defaults; ipywidgets uses symmetric range around zero).

Not done: enter-to-submit in manual mode, type-hint-only (no default) parity with ipywidgets (we already accept no-default; ipywidgets maps `x: int` → `IntText()`), `auto_display` in notebooks (fundamentally Jupyter-only).

## Shiny Express patterns

Transferable: context-manager layouts (already used in dash-interact `page.columns()` etc), auto-output-ui (already done via `FnPanel`), reactive-calc analog (our `_cache=True`), `@reactive.event` analog (proposed `_trigger="field_name"` parameter).

Not transferable: AST transformation at import, dynamic dependency tracking, push-pull invalidation — all require architecture Dash doesn't have.

## Module layout

- [src/dash_fn_form/_forms.py](src/dash_fn_form/_forms.py) — `FnForm`, top-level form construction
- [src/dash_fn_form/_spec.py](src/dash_fn_form/_spec.py) — signature introspection, `Field`
- [src/dash_fn_form/_field_components.py](src/dash_fn_form/_field_components.py) — type → Dash component
- [src/dash_fn_form/_form_layouts.py](src/dash_fn_form/_form_layouts.py) — sections/accordion/tabs rendering
- [src/dash_fn_form/_renderers.py](src/dash_fn_form/_renderers.py) — auto-render of return values
- [src/dash_fn_form/fn_interact.py](src/dash_fn_form/fn_interact.py) — `build_fn_panel`
- [src/dash_fn_form/layout.py](src/dash_fn_form/layout.py) — public layout dataclasses

## Tooling

- `uv`, `ruff`, `ty`, `prek`, `setuptools-scm`
- Python 3.10–3.14
- CI: GitHub Actions — lint (prek + ty), test, publish (PyPI OIDC)
- MIT licensed
- Independent git repo; also an editable member of the brand-toolkit uv workspace
