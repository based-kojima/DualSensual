"""Theme color constants for Dual Sensual."""

from dataclasses import dataclass
from PyQt6.QtGui import QColor


@dataclass(frozen=True)
class Theme:
    """Dark erotic color palette with burgundy and rose gold accents."""

    # Primary colors
    PRIMARY_DARK = "#1A0A10"      # Deep dark background
    PRIMARY = "#4A1528"            # Burgundy surfaces
    PRIMARY_LIGHT = "#722F37"      # Lighter burgundy for buttons

    # Accent colors
    ACCENT = "#B76E79"             # Rose gold highlights
    ACCENT_GLOW = "#E8B4B8"        # Lighter rose for glow effects

    # Text colors
    TEXT = "#F5E6E8"               # Soft white-pink text
    TEXT_DIM = "#A08085"           # Dimmed text

    # Status colors
    SUCCESS = "#4CAF50"            # Connected status
    WARNING = "#FFA726"            # Bluetooth warning
    ERROR = "#EF5350"              # Disconnected status

    @classmethod
    def get_color(cls, hex_color: str) -> QColor:
        """Convert hex string to QColor."""
        return QColor(hex_color)

    @classmethod
    def get_glow_gradient(cls) -> str:
        """Get CSS gradient for glow effects."""
        return f"qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 {cls.ACCENT_GLOW}, stop:1 transparent)"
