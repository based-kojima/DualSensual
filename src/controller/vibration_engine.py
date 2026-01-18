"""Vibration engine with threaded pattern execution."""

import threading
from typing import Optional

from PyQt6.QtCore import QObject, QThread, pyqtSignal

from controller.dualsense_manager import DualSenseManager
from controller.patterns import PatternType, get_pattern_generator


class VibrationWorker(QObject):
    """Worker that runs vibration patterns in a separate thread."""

    intensity_updated = pyqtSignal(int)
    error_occurred = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._stop_event = threading.Event()
        self._running = False
        self._intensity = 128
        self._pattern_type = PatternType.CONSTANT
        self._manager = DualSenseManager()
        self._lock = threading.Lock()

    @property
    def intensity(self) -> int:
        """Get current intensity."""
        with self._lock:
            return self._intensity

    @intensity.setter
    def intensity(self, value: int) -> None:
        """Set intensity (0-255)."""
        with self._lock:
            self._intensity = max(0, min(255, value))

    @property
    def pattern_type(self) -> PatternType:
        """Get current pattern type."""
        with self._lock:
            return self._pattern_type

    @pattern_type.setter
    def pattern_type(self, value: PatternType) -> None:
        """Set pattern type."""
        with self._lock:
            self._pattern_type = value

    def start_pattern(self) -> None:
        """Start the vibration pattern loop."""
        self._stop_event.clear()
        self._running = True
        self._run_pattern_loop()

    def stop_pattern(self) -> None:
        """Stop the vibration pattern loop."""
        self._stop_event.set()
        self._running = False
        self._manager.stop_motors()

    def _run_pattern_loop(self) -> None:
        """Main pattern execution loop."""
        while not self._stop_event.is_set():
            try:
                # Get current settings
                with self._lock:
                    intensity = self._intensity
                    pattern_type = self._pattern_type

                # Create pattern generator
                pattern = get_pattern_generator(pattern_type, intensity)

                # Run pattern until settings change or stop requested
                for left, right, duration in pattern:
                    if self._stop_event.is_set():
                        break

                    # Check if settings changed
                    with self._lock:
                        if (self._intensity != intensity or
                            self._pattern_type != pattern_type):
                            break

                    # Apply motor values
                    self._manager.set_motors(left, right)
                    self.intensity_updated.emit(max(left, right))

                    # Wait for duration
                    self._stop_event.wait(duration)

            except Exception as e:
                self.error_occurred.emit(str(e))
                break

        # Ensure motors are stopped
        self._manager.stop_motors()


class VibrationEngine(QObject):
    """Engine that manages vibration worker thread."""

    intensity_updated = pyqtSignal(int)
    error_occurred = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._thread: Optional[QThread] = None
        self._worker: Optional[VibrationWorker] = None
        self._active = False

    @property
    def is_active(self) -> bool:
        """Check if engine is currently running."""
        return self._active

    def start_vibration(
        self, intensity: int = 128, pattern_type: PatternType = PatternType.CONSTANT
    ) -> None:
        """Start vibration with specified settings.

        Args:
            intensity: Motor intensity (0-255)
            pattern_type: Type of vibration pattern
        """
        if self._active:
            self.stop_vibration()

        # Create worker and thread
        self._thread = QThread()
        self._worker = VibrationWorker()
        self._worker.intensity = intensity
        self._worker.pattern_type = pattern_type

        # Move worker to thread
        self._worker.moveToThread(self._thread)

        # Connect signals
        self._thread.started.connect(self._worker.start_pattern)
        self._worker.intensity_updated.connect(self.intensity_updated)
        self._worker.error_occurred.connect(self._on_error)

        # Start thread
        self._active = True
        self._thread.start()

    def stop_vibration(self) -> None:
        """Stop vibration and cleanup thread."""
        if not self._active:
            return

        self._active = False

        if self._worker is not None:
            self._worker.stop_pattern()

        if self._thread is not None:
            self._thread.quit()
            self._thread.wait(1000)
            self._thread = None

        self._worker = None

    def set_intensity(self, intensity: int) -> None:
        """Update vibration intensity.

        Args:
            intensity: Motor intensity (0-255)
        """
        if self._worker is not None:
            self._worker.intensity = intensity

    def set_pattern(self, pattern_type: PatternType) -> None:
        """Update vibration pattern.

        Args:
            pattern_type: Type of vibration pattern
        """
        if self._worker is not None:
            self._worker.pattern_type = pattern_type

    def _on_error(self, error: str) -> None:
        """Handle worker error."""
        self.stop_vibration()
        self.error_occurred.emit(error)
