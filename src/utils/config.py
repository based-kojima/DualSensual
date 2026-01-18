"""Application configuration settings."""

from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration constants."""

    # Window settings
    WINDOW_WIDTH: int = 400
    WINDOW_HEIGHT: int = 600
    WINDOW_TITLE: str = "Dual Sensual"

    # Default values
    DEFAULT_INTENSITY: int = 50  # Percentage (0-100)
    DEFAULT_PATTERN: str = "Constant"

    # Connection settings
    CONNECTION_CHECK_INTERVAL: int = 2000  # milliseconds

    # Animation settings
    TOGGLE_ANIMATION_DURATION: int = 200  # milliseconds
    GLOW_ANIMATION_INTERVAL: int = 50  # milliseconds
