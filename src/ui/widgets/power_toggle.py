"""Animated power toggle widget with glow effect."""

from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient
from PyQt6.QtWidgets import QWidget

from ui.styles.theme import Theme


class PowerToggle(QWidget):
    """Animated toggle switch with pulsing glow when active."""

    toggled = pyqtSignal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._checked = False
        self._handle_position = 0.0
        self._glow_intensity = 0.0
        self._glow_direction = 1

        # Widget size
        self.setFixedSize(80, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Handle animation
        self._handle_animation = QPropertyAnimation(self, b"handlePosition")
        self._handle_animation.setDuration(200)
        self._handle_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Glow animation timer
        self._glow_timer = QTimer(self)
        self._glow_timer.timeout.connect(self._update_glow)
        self._glow_timer.setInterval(50)

    def _get_handle_position(self) -> float:
        return self._handle_position

    def _set_handle_position(self, value: float) -> None:
        self._handle_position = value
        self.update()

    handlePosition = pyqtProperty(float, _get_handle_position, _set_handle_position)

    @property
    def is_checked(self) -> bool:
        """Get checked state."""
        return self._checked

    def set_checked(self, checked: bool, animated: bool = True) -> None:
        """Set checked state.

        Args:
            checked: New checked state
            animated: Whether to animate the transition
        """
        if self._checked == checked:
            return

        self._checked = checked

        if animated:
            self._handle_animation.setStartValue(self._handle_position)
            self._handle_animation.setEndValue(1.0 if checked else 0.0)
            self._handle_animation.start()
        else:
            self._handle_position = 1.0 if checked else 0.0

        if checked:
            self._glow_timer.start()
        else:
            self._glow_timer.stop()
            self._glow_intensity = 0.0

        self.update()
        self.toggled.emit(checked)

    def _update_glow(self) -> None:
        """Update glow animation."""
        self._glow_intensity += 0.1 * self._glow_direction
        if self._glow_intensity >= 1.0:
            self._glow_direction = -1
        elif self._glow_intensity <= 0.3:
            self._glow_direction = 1
        self.update()

    def mousePressEvent(self, event) -> None:
        """Handle mouse press to toggle."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_checked(not self._checked)

    def paintEvent(self, event) -> None:
        """Paint the toggle switch."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        handle_radius = height // 2 - 4

        # Draw glow when active
        if self._checked and self._glow_intensity > 0:
            glow_color = QColor(Theme.ACCENT_GLOW)
            glow_color.setAlphaF(self._glow_intensity * 0.5)

            gradient = QRadialGradient(width / 2, height / 2, width / 2)
            gradient.setColorAt(0, glow_color)
            gradient.setColorAt(1, QColor(0, 0, 0, 0))

            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(-10, -10, width + 20, height + 20)

        # Draw track
        track_color = QColor(Theme.PRIMARY_LIGHT) if not self._checked else QColor(Theme.ACCENT)
        painter.setBrush(QBrush(track_color))
        painter.setPen(QPen(QColor(Theme.ACCENT), 2))
        painter.drawRoundedRect(2, 2, width - 4, height - 4, height // 2, height // 2)

        # Calculate handle position
        handle_x = 4 + self._handle_position * (width - height)
        handle_y = height // 2

        # Draw handle shadow
        shadow_color = QColor(0, 0, 0, 50)
        painter.setBrush(QBrush(shadow_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(handle_x + 2), int(handle_y - handle_radius + 2),
                           handle_radius * 2, handle_radius * 2)

        # Draw handle
        handle_color = QColor(Theme.ACCENT_GLOW) if self._checked else QColor(Theme.TEXT)
        painter.setBrush(QBrush(handle_color))
        painter.setPen(QPen(QColor(Theme.ACCENT), 2))
        painter.drawEllipse(int(handle_x), int(handle_y - handle_radius),
                           handle_radius * 2, handle_radius * 2)
