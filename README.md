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
