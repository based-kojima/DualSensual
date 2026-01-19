# Dual Sensual

DualSensual is a playful but serious experiment in repurposing the PS5 DualSense controller as a high-fidelity haptic device.
While originally designed for games, the DualSense hardware lends itself surprisingly well to adult, artistic, and alternative interactive experiences. This project exposes and remaps those features in real time.
For consenting adults, curiosity, and creative misuse of hardware.

## Features

- **Power Toggle** - Easy on/off control for vibration
- **Intensity Slider** - Adjust vibration strength (0-255)
- **Vibration Patterns**
  - Constant - Steady vibration
  - Pulse - Rhythmic on/off pattern
  - Wave - Smooth sine wave intensity modulation
  - Heartbeat - Realistic double-pulse heartbeat pattern
- **Real-time Status Display** - Controller connection status

## Requirements

- Windows 10/11
- PlayStation DualSense controller connected via USB or Bluetooth

## Installation

### Option 1: Download Release
Download `DualSensual.exe` from the [Releases](https://github.com/based-kojima/DualSensual/releases) page.

### Option 2: Run from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/based-kojima/DualSensual.git
   cd DualSensual
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python src/main.py
   ```

## Building from Source

To build the executable yourself:

```bash
pip install pyinstaller
pyinstaller dualsensual.spec --noconfirm
```

The executable will be created in the `dist` folder.

## Dependencies

- PyQt6 - GUI framework
- pydualsense - DualSense controller interface
- hidapi - HID device communication

## License

MIT License
