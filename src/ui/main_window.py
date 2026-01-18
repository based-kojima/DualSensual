"""Main application window."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QComboBox,
)

from ui.widgets.power_toggle import PowerToggle
from ui.widgets.intensity_slider import IntensitySlider
from ui.widgets.status_display import StatusDisplay
from ui.styles.theme import Theme
from controller.vibration_engine import VibrationEngine
from controller.patterns import PatternType
from controller.dualsense_manager import DualSenseManager


class MainWindow(QMainWindow):
    """Main application window for Dual Sensual."""

    def __init__(self) -> None:
        super().__init__()
        self._manager = DualSenseManager()
        self._engine = VibrationEngine()
        self._setup_window()
        self._setup_ui()
        self._connect_signals()

    def _setup_window(self) -> None:
        """Configure window properties."""
        self.setWindowTitle("Dual Sensual")
        self.setFixedSize(400, 600)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowCloseButtonHint |
            Qt.WindowType.WindowMinimizeButtonHint
        )

        # Set background color
        self.setStyleSheet(f"background-color: {Theme.PRIMARY_DARK};")

    def _setup_ui(self) -> None:
        """Set up the main UI layout."""
        # Central widget
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        # Main layout
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("DUAL SENSUAL")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Status section
        status_group = self._create_group_box("")
        status_layout = QVBoxLayout(status_group)
        status_layout.setContentsMargins(0, 0, 0, 0)
        self._status_display = StatusDisplay()
        status_layout.addWidget(self._status_display)
        layout.addWidget(status_group)

        # Power toggle section
        power_group = self._create_group_box("Power")
        power_layout = QVBoxLayout(power_group)
        power_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._power_toggle = PowerToggle()
        power_layout.addWidget(self._power_toggle, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(power_group)

        # Intensity section
        intensity_group = self._create_group_box("")
        intensity_layout = QVBoxLayout(intensity_group)
        self._intensity_slider = IntensitySlider()
        intensity_layout.addWidget(self._intensity_slider)
        layout.addWidget(intensity_group)

        # Pattern section
        pattern_group = self._create_group_box("Vibration Pattern")
        pattern_layout = QVBoxLayout(pattern_group)

        self._pattern_combo = QComboBox()
        for pattern in PatternType:
            self._pattern_combo.addItem(pattern.value, pattern)
        pattern_layout.addWidget(self._pattern_combo)

        layout.addWidget(pattern_group)

        # Spacer
        layout.addStretch()

    def _create_group_box(self, title: str) -> QGroupBox:
        """Create a styled group box."""
        group = QGroupBox(title)
        return group

    def _connect_signals(self) -> None:
        """Connect widget signals to handlers."""
        self._power_toggle.toggled.connect(self._on_power_toggled)
        self._intensity_slider.value_changed.connect(self._on_intensity_changed)
        self._pattern_combo.currentIndexChanged.connect(self._on_pattern_changed)
        self._engine.error_occurred.connect(self._on_engine_error)

    def _on_power_toggled(self, checked: bool) -> None:
        """Handle power toggle state change."""
        if checked:
            if not self._manager.is_connected:
                if not self._manager.connect():
                    self._power_toggle.set_checked(False, animated=True)
                    return

            intensity = self._intensity_slider.intensity
            pattern = self._pattern_combo.currentData()
            self._engine.start_vibration(intensity, pattern)
        else:
            self._engine.stop_vibration()

    def _on_intensity_changed(self, intensity: int) -> None:
        """Handle intensity slider change."""
        if self._engine.is_active:
            self._engine.set_intensity(intensity)

    def _on_pattern_changed(self, index: int) -> None:
        """Handle pattern selection change."""
        if self._engine.is_active:
            pattern = self._pattern_combo.currentData()
            self._engine.set_pattern(pattern)

    def _on_engine_error(self, error: str) -> None:
        """Handle vibration engine error."""
        self._power_toggle.set_checked(False, animated=True)

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Stop vibration and disconnect controller
        self._engine.stop_vibration()
        self._manager.disconnect()
        event.accept()
