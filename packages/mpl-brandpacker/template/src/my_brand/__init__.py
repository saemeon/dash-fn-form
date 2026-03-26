"""my-brand — example branded matplotlib package.

Usage::

    import my_brand.pyplot as plt

    fig, ax = plt.subplots(figsize=my_brand.Sizes.half)
    ax.plot([1, 2, 3], [4, 5, 6], color=my_brand.Colors.primary)
    fig.set_title("Q4 Revenue")
    fig.set_sources("Internal Data")
    plt.show()

    # Scale fonts for a presentation:
    with my_brand.FontSizes.scaled("presentation"):
        fig, ax = plt.subplots(figsize=my_brand.Sizes.presentation)
        ...
"""

from pathlib import Path

import mpl_brandpacker

from my_brand.axes import MyAxes, make_ax, set_style
from my_brand.colors import Colors
from my_brand.figure import MyFigure, make_fig
from my_brand.sizes import FontSizes, Sizes

mpl_brandpacker.configure(
    figure_cls=MyFigure,
    axes_cls=MyAxes,
    style_fn=set_style,
    stylesheet=Path(__file__).parent,
)
