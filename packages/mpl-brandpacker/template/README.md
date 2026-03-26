# my-brand

Branded matplotlib package built with [mpl-brandpacker](https://github.com/saemeon/mpl-brandpacker).

## Install

```bash
pip install -e .
```

## Usage

```python
import my_brand.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
fig.set_title("Q4 Revenue")
fig.set_sources("Internal Data")
ax.set_xlabel("Quarter")
plt.show()
```

## Customize

| File | What to change |
|---|---|
| `colors.py` | Brand colors (hex values) |
| `sizes.py` | Named figure sizes (width, height in inches) |
| `figure.py` | Figure-level branding (title, subtitle, sources, footnote) |
| `axes.py` | Axes-level branding (labels, grid, spines) |
| `header.py` | Header/footer layout helper |
| `legend.py` | Legend placement helpers |
| `pyplot.py` | Usually no changes needed |

## Documentation helpers

```python
import my_brand

my_brand.Colors.plot()  # → swatch grid of all colors
my_brand.Sizes.plot()   # → visual comparison of all sizes
```
