"""Resource path helper for PyInstaller compatibility."""

import os
import sys
from pathlib import Path


def get_resource_path(relative_path: str) -> Path:
    """Get absolute path to resource, works for dev and PyInstaller.

    Args:
        relative_path: Path relative to the project root

    Returns:
        Absolute path to the resource
    """
    if hasattr(sys, "_MEIPASS"):
        # Running as PyInstaller bundle
        base_path = Path(sys._MEIPASS)
    else:
        # Running in development
        base_path = Path(__file__).parent.parent.parent

    return base_path / relative_path


def get_stylesheet_path() -> Path:
    """Get path to the QSS stylesheet."""
    return get_resource_path("src/ui/styles/stylesheet.qss")


def get_icon_path(icon_name: str = "app_icon.ico") -> Path:
    """Get path to an icon file.

    Args:
        icon_name: Name of the icon file

    Returns:
        Absolute path to the icon
    """
    return get_resource_path(f"assets/icons/{icon_name}")
