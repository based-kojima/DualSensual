"""Styled intensity slider widget."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider

from ui.styles.theme import Theme


class IntensitySlider(QWidget):
    """Intensity slider with label and percentage display."""

    value_changed = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header with label and value
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel("Intensity")
        self._label.setObjectName("sectionLabel")
        header_layout.addWidget(self._label)

        header_layout.addStretch()

        self._value_label = QLabel("50%")
        self._value_label.setObjectName("valueLabel")
        header_layout.addWidget(self._value_label)

        layout.addLayout(header_layout)

        # Slider
        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setMinimum(0)
        self._slider.setMaximum(100)
        self._slider.setValue(50)
        self._slider.setTickPosition(QSlider.TickPosition.NoTicks)
        self._slider.valueChanged.connect(self._on_value_changed)
        layout.addWidget(self._slider)

    def _on_value_changed(self, value: int) -> None:
        """Handle slider value change."""
        self._value_label.setText(f"{value}%")
        # Convert percentage (0-100) to motor intensity (0-255)
        intensity = int(value * 255 / 100)
        self.value_changed.emit(intensity)

    @property
    def value(self) -> int:
        """Get current value (0-100)."""
        return self._slider.value()

    @value.setter
    def value(self, val: int) -> None:
        """Set current value (0-100)."""
        self._slider.setValue(val)

    @property
    def intensity(self) -> int:
        """Get motor intensity (0-255)."""
        return int(self._slider.value() * 255 / 100)

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the slider."""
        self._slider.setEnabled(enabled)
        opacity = "1.0" if enabled else "0.5"
        self.setStyleSheet(f"QWidget {{ opacity: {opacity}; }}")
