"""Vibration pattern generators."""

from enum import Enum
from typing import Generator
import math


class PatternType(Enum):
    """Available vibration patterns."""
    CONSTANT = "Constant"
    PULSE = "Pulse"
    WAVE = "Wave"
    HEARTBEAT = "Heartbeat"


def constant_pattern(intensity: int) -> Generator[tuple[int, int, float], None, None]:
    """Generate constant vibration.

    Args:
        intensity: Motor intensity (0-255)

    Yields:
        Tuple of (left_motor, right_motor, duration_seconds)
    """
    while True:
        yield (intensity, intensity, 0.05)


def pulse_pattern(intensity: int) -> Generator[tuple[int, int, float], None, None]:
    """Generate rhythmic pulse pattern.

    Args:
        intensity: Motor intensity (0-255)

    Yields:
        Tuple of (left_motor, right_motor, duration_seconds)
    """
    while True:
        yield (intensity, intensity, 0.3)  # On
        yield (0, 0, 0.3)  # Off


def wave_pattern(intensity: int) -> Generator[tuple[int, int, float], None, None]:
    """Generate sine wave intensity modulation.

    Args:
        intensity: Base motor intensity (0-255)

    Yields:
        Tuple of (left_motor, right_motor, duration_seconds)
    """
    step = 0
    steps_per_cycle = 40
    while True:
        # Calculate sine wave value (0 to 1)
        wave_value = (math.sin(2 * math.pi * step / steps_per_cycle) + 1) / 2
        current_intensity = int(intensity * wave_value)
        yield (current_intensity, current_intensity, 0.05)
        step = (step + 1) % steps_per_cycle


def heartbeat_pattern(intensity: int) -> Generator[tuple[int, int, float], None, None]:
    """Generate heartbeat-like double pulse pattern.

    Args:
        intensity: Motor intensity (0-255)

    Yields:
        Tuple of (left_motor, right_motor, duration_seconds)
    """
    while True:
        # First beat (strong)
        yield (intensity, intensity, 0.1)
        yield (0, 0, 0.1)
        # Second beat (slightly weaker)
        yield (int(intensity * 0.7), int(intensity * 0.7), 0.1)
        yield (0, 0, 0.6)  # Pause before next heartbeat


def get_pattern_generator(
    pattern_type: PatternType, intensity: int
) -> Generator[tuple[int, int, float], None, None]:
    """Get the appropriate pattern generator.

    Args:
        pattern_type: The type of pattern to generate
        intensity: Motor intensity (0-255)

    Returns:
        Generator yielding (left_motor, right_motor, duration_seconds) tuples
    """
    generators = {
        PatternType.CONSTANT: constant_pattern,
        PatternType.PULSE: pulse_pattern,
        PatternType.WAVE: wave_pattern,
        PatternType.HEARTBEAT: heartbeat_pattern,
    }

    generator_func = generators.get(pattern_type, constant_pattern)
    return generator_func(intensity)
