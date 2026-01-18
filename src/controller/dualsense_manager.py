"""DualSense controller connection manager (singleton pattern)."""

from enum import Enum
from typing import Optional
import threading

from pydualsense import pydualsense


class ConnectionType(Enum):
    """Controller connection type."""
    NONE = "None"
    USB = "USB"
    BLUETOOTH = "Bluetooth"


class DualSenseManager:
    """Singleton manager for DualSense controller connection."""

    _instance: Optional["DualSenseManager"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "DualSenseManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._controller: Optional[pydualsense] = None
        self._connected = False
        self._connection_type = ConnectionType.NONE

    @property
    def is_connected(self) -> bool:
        """Check if controller is connected."""
        return self._connected and self._controller is not None

    @property
    def connection_type(self) -> ConnectionType:
        """Get the current connection type."""
        return self._connection_type

    @property
    def controller(self) -> Optional[pydualsense]:
        """Get the controller instance."""
        return self._controller

    def connect(self) -> bool:
        """Attempt to connect to a DualSense controller.

        Returns:
            True if connection successful, False otherwise.
        """
        if self._connected:
            return True

        try:
            self._controller = pydualsense()
            self._controller.init()
            self._connected = True

            # Determine connection type based on controller properties
            # pydualsense doesn't expose this directly, but USB is more common
            # and required for full haptic control
            self._connection_type = ConnectionType.USB

            return True
        except Exception:
            self._controller = None
            self._connected = False
            self._connection_type = ConnectionType.NONE
            return False

    def disconnect(self) -> None:
        """Disconnect from the controller."""
        if self._controller is not None:
            try:
                # Stop any vibration before disconnecting
                self._controller.setLeftMotor(0)
                self._controller.setRightMotor(0)
                self._controller.close()
            except Exception:
                pass
            finally:
                self._controller = None
                self._connected = False
                self._connection_type = ConnectionType.NONE

    def set_motors(self, left: int, right: int) -> None:
        """Set motor intensities.

        Args:
            left: Left motor intensity (0-255)
            right: Right motor intensity (0-255)
        """
        if not self.is_connected or self._controller is None:
            return

        # Clamp values to valid range
        left = max(0, min(255, left))
        right = max(0, min(255, right))

        try:
            self._controller.setLeftMotor(left)
            self._controller.setRightMotor(right)
        except Exception:
            pass

    def stop_motors(self) -> None:
        """Stop all motor vibration."""
        self.set_motors(0, 0)
