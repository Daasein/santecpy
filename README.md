# SantecLaserPy

This project is designed to communicate with VISA and Santec tunable laser using Python. It includes classes and methods for controlling and interfacing with the laser hardware.

## Installation

To install the library directly from GitHub, use the following command:

```bash
pip install git+https://github.com/Daasein/santecpy.git
```

## Usage

### Instantiating the Laser Controller

Below is an example of how to instantiate and use the laser controller:

```python
from santecpy import SantecLaser

# Initialize the laser controller
laser = SantecLaser(address="GPIB0::30::INSTR")

# Example: Set the wavelength
laser.set_wavelength(1550.0)

# Example: Turn the laser on
laser.LD_on()

# Example: Turn the laser off
laser.LD_off()
```

Replace `address` with the appropriate VISA resource string for your laser device.
