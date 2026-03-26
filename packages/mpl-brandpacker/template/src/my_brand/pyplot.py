"""Branded pyplot — drop-in replacement for matplotlib.pyplot.

Usage::

    import my_brand.pyplot as plt

    fig, ax = plt.subplots()
    fig.set_title("Q4 Revenue")
    ax.plot([1, 2, 3], [4, 5, 6])
    plt.show()
"""

import my_brand  # noqa — triggers configure()
from mpl_brandpacker.pyplot import *  # noqa
