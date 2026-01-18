"""Connection status display widget."""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from ui.styles.theme import Theme
from controller.dualsense_manager import DualSenseManager, ConnectionType


class StatusDisplay(QWidget):
    """Display for controller connection status."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._manager = DualSenseManager()
        self._setup_ui()
        self._setup_refresh_timer()

    def _setup_ui(self) -> None:
        """Set up the widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # Controller status row
        controller_row = QHBoxLayout()
        controller_row.setSpacing(10)

        controller_label = QLabel("Controller:")
        controller_label.setObjectName("sectionLabel")
        controller_row.addWidget(controller_label)

        self._status_label = QLabel("Disconnected")
        controller_row.addWidget(self._status_label)

        self._status_indicator = QLabel("\u25cf")  # Filled circle
        self._status_indicator.setFixedWidth(20)
        controller_row.addWidget(self._status_indicator)

        controller_row.addStretch()
        layout.addLayout(controller_row)

        # Connection type row
        connection_row = QHBoxLayout()
        connection_row.setSpacing(10)

        connection_label = QLabel("Connection:")
        connection_label.setObjectName("sectionLabel")
        connection_row.addWidget(connection_label)

        self._connection_label = QLabel("None")
        connection_row.addWidget(self._connection_label)

        connection_row.addStretch()
        layout.addLayout(connection_row)

        # Warning label (for Bluetooth)
        self._warning_label = QLabel()
        self._warning_label.setWordWrap(True)
        self._warning_label.setStyleSheet(f"color: {Theme.WARNING}; font-size: 11px;")
        self._warning_label.hide()
        layout.addWidget(self._warning_label)

        # Initial update
        self._update_status()

    def _setup_refresh_timer(self) -> None:
        """Set up timer to periodically check connection status."""
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._check_connection)
        self._refresh_timer.start(2000)  # Check every 2 seconds

    def _check_connection(self) -> None:
        """Check and update connection status."""
        if not self._manager.is_connected:
            # Try to connect
            self._manager.connect()
        self._update_status()

    def _update_status(self) -> None:
        """Update the status display."""
        if self._manager.is_connected:
            self._status_label.setText("Connected")
            self._status_label.setStyleSheet(f"color: {Theme.SUCCESS};")
            self._status_indicator.setStyleSheet(f"color: {Theme.SUCCESS};")

            conn_type = self._manager.connection_type
            self._connection_label.setText(conn_type.value)

            if conn_type == ConnectionType.BLUETOOTH:
                self._warning_label.setText(
                    "Note: Full haptic control requires USB connection."
                )
                self._warning_label.show()
            else:
                self._warning_label.hide()
        else:
            self._status_label.setText("Disconnected")
            self._status_label.setStyleSheet(f"color: {Theme.ERROR};")
            self._status_indicator.setStyleSheet(f"color: {Theme.ERROR};")
            self._connection_label.setText("None")
            self._warning_label.hide()

    @property
    def is_connected(self) -> bool:
        """Check if controller is connected."""
        return self._manager.is_connected

    def refresh(self) -> None:
        """Manually refresh connection status."""
        self._check_connection()
