# Copyright (c) Simon Niederberger.
# Distributed under the terms of the MIT License.

"""Corporate frame — wraps a PNG image with header and footer using matplotlib.

This is the core module. No Dash dependency. Works standalone::

    from corpframe import apply_frame

    with open("chart.png", "rb") as f:
        raw = f.read()

    framed = apply_frame(raw, title="Q4 Revenue", sources="Source: Bloomberg")

    with open("chart_framed.png", "wb") as f:
        f.write(framed)
"""

from __future__ import annotations

import io

import matplotlib.pyplot as plt

plt.switch_backend("agg")


def apply_frame(
    png_bytes: bytes,
    title: str = "",
    subtitle: str = "",
    footnotes: str = "",
    sources: str = "",
    dpi: int = 300,
) -> bytes:
    """Wrap a PNG image with a corporate header and footer.

    Parameters
    ----------
    png_bytes :
        Raw PNG image data.
    title :
        Header title (bold, with accent underline).
    subtitle :
        Header subtitle (italic, below title).
    footnotes :
        Footer text, left-aligned.
    sources :
        Footer text, right-aligned.
    dpi :
        Output resolution.

    Returns
    -------
    bytes
        Framed PNG image data.
    """
    img = plt.imread(io.BytesIO(png_bytes))
    img_h, img_w = img.shape[:2]

    header_h = int(img_h * 0.12) if (title or subtitle) else 0
    footer_h = int(img_h * 0.08) if (footnotes or sources) else 0
    total_h = img_h + header_h + footer_h

    fig = plt.figure(
        figsize=(img_w / dpi, total_h / dpi), dpi=dpi, facecolor="white",
    )

    # --- header ---
    if header_h > 0:
        ax = fig.add_axes([0, 1 - header_h / total_h, 1, header_h / total_h])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_facecolor("white")
        ax.axis("off")

        if title:
            ax.text(
                0.03, 0.65, title,
                fontsize=11, fontweight="bold", color="#1a1a2e",
                va="center", transform=ax.transAxes,
            )
            ax.plot(
                [0.03, 0.35], [0.42, 0.42],
                color="#e94560", linewidth=2,
                transform=ax.transAxes, clip_on=False,
            )
        if subtitle:
            ax.text(
                0.03, 0.15, subtitle,
                fontsize=8, color="#555555", style="italic",
                va="center", transform=ax.transAxes,
            )

    # --- image ---
    ax_img = fig.add_axes([0, footer_h / total_h, 1, img_h / total_h])
    ax_img.imshow(img)
    ax_img.axis("off")

    # --- footer ---
    if footer_h > 0:
        ax = fig.add_axes([0, 0, 1, footer_h / total_h])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_facecolor("white")
        ax.axis("off")

        ax.plot(
            [0.03, 0.97], [0.85, 0.85],
            color="#dddddd", linewidth=0.5,
            transform=ax.transAxes, clip_on=False,
        )
        if footnotes:
            ax.text(
                0.03, 0.4, footnotes,
                fontsize=6, color="#888888",
                va="center", transform=ax.transAxes,
            )
        if sources:
            ax.text(
                0.97, 0.4, sources,
                fontsize=6, color="#888888",
                va="center", ha="right", transform=ax.transAxes,
            )

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return buf.read()
