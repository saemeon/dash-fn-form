[![PyPI](https://img.shields.io/pypi/v/dash-fn-form)](https://pypi.org/project/dash-fn-form/)
[![Python](https://img.shields.io/pypi/pyversions/dash-fn-form)](https://pypi.org/project/dash-fn-form/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Dash](https://img.shields.io/badge/Dash-008DE4?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![prek](https://img.shields.io/badge/prek-checked-blue)](https://github.com/saemeon/prek)

# dash-fn-form

Introspection-based UI engine for Plotly Dash — transform type-hinted Python functions into reactive Dash forms.

## Installation

```bash
pip install dash-fn-form
```

Most users should install [dash-interact](https://github.com/saemeon/dash-interact) instead, which includes this package and adds a convenience `page` API.

## Usage

```python
from dash import Dash, html
from dash_fn_form import build_fn_panel

def sine_wave(amplitude: float = 1.0, frequency: float = 2.0):
    import numpy as np, plotly.graph_objects as go
    x = np.linspace(0, 6 * np.pi, 600)
    return go.Figure(go.Scatter(x=x, y=amplitude * np.sin(frequency * x)))

app = Dash(__name__)
app.layout = html.Div([build_fn_panel(sine_wave)])
app.run(debug=True)
```

`build_fn_panel` inspects the function signature and builds a form with matching controls. The return value is rendered automatically.

## Type mapping

| Python type | Control |
|---|---|
| `float` | Number input (or slider with `(min, max, step)`) |
| `int` | Number input (integer step) |
| `bool` | Checkbox |
| `Literal[A, B, C]` | Dropdown |
| `str` | Text input |
| `date` / `datetime` | Date picker |
| `list[T]` / `tuple[T, ...]` | Comma-separated input |
| `T \| None` | Same as `T`, submits `None` when empty |

## Field customization

```python
from dash_fn_form import Field

form = FnForm("my_form", my_fn, title=Field(label="Title", col_span=2))
```

## License

MIT
