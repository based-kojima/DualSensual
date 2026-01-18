"""Dual Sensual - DualSense Controller Vibration Application."""

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from ui.main_window import MainWindow
from utils.resources import get_stylesheet_path, get_icon_path


def load_stylesheet(app: QApplication) -> None:
    """Load and apply the QSS stylesheet."""
    stylesheet_path = get_stylesheet_path()
    if stylesheet_path.exists():
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


def main() -> int:
    """Application entry point."""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Dual Sensual")
    app.setOrganizationName("DualSensual")

    # Set application icon
    icon_path = get_icon_path()
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # Load stylesheet
    load_stylesheet(app)

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
