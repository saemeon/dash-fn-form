# Copyright (c) Simon Niederberger.
# Distributed under the terms of the MIT License.

"""CLI entry point for corpframe — used by R subprocess calls.

Usage::

    corpframe --input chart.png --output framed.png \\
        --title "Q4 Results" --subtitle "Revenue by Region"

    # Or via python -m:
    python -m corpframe --input chart.png --output framed.png --title "Q4"
"""

from __future__ import annotations

import argparse

from corpframe.frame import apply_frame


def main():
    parser = argparse.ArgumentParser(description="Apply corporate frame to PNG")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--footnotes", default="")
    parser.add_argument("--sources", default="")
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()

    with open(args.input, "rb") as f:
        png_bytes = f.read()

    framed = apply_frame(
        png_bytes, title=args.title, subtitle=args.subtitle,
        footnotes=args.footnotes, sources=args.sources, dpi=args.dpi,
    )

    with open(args.output, "wb") as f:
        f.write(framed)


if __name__ == "__main__":
    main()
