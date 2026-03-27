"""Layout configuration for form field grouping."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Section:
    """A named group of fields."""

    name: str
    fields: list[str]
    default_open: bool = True
    description: str | None = None


@dataclass
class Accordion:
    """Collapsible section layout."""

    sections: list[Section]
    remaining_fields: str = "bottom"  # "top" | "bottom" | "none"
    multiple: bool = True


@dataclass
class Tabs:
    """Tabbed section layout."""

    sections: list[Section]
    remaining_fields: str = "bottom"
