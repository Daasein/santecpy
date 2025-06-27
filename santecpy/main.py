# main.py

import pyvisa
import math


class SantecLaser:
    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        try:
            self.gpib = self.rm.open_resource(address)
            self.is_connected = True
        except Exception as e:
            self.is_connected = False
            raise ConnectionError("Connection failed") from e
        self._wavelength = None  # Private attribute for wavelength
        self._optical_power = None  # Private attribute for optical power
        self.wavelength_range = (1530, 1610)  # Wavelength range in nm

    @property
    def su_code(self):
        self.gpib.query("SU\n")
        return self.gpib.read().replace("\n", "")

    def su_code_parse(self, su_result):
        values = {}
        rst = su_result.strip()
        if len(rst) != 8:
            raise ValueError("String length read from SU is not 8, please check.")
        values["current"] = rst[0] == "-"
        values["coherence"] = rst[1] == "1"
        values["frequency_locking"] = rst[2] != "0"
        values["fine_tuning"] = rst[2] == "0"
        values["acc"] = rst[4] in ["1", "3"]
        values["att"] = rst[4] in ["2", "3"]
        values["LD_temperature"] = rst[5] in ["1", "3"]
        values["frequency_locking_temperature"] = rst[5] in ["2", "3"]
        values["LD_current_limit"] = rst[6] == "1"
        values["wavelength_tuning"] = rst[7] in ["7", "5", "3", "1"]
        values["current_driver_tuning"] = rst[7] in ["7", "6", "3", "2"]
        values["att_tuning"] = rst[7] in ["7", "6", "5", "4"]
        return values

    def read_status(self):
        su_code = self.read_su_code()
        return self.su_code_parse(su_code)

    @property
    def wavelength(self):
        return self.read_wavelength()  # Automatically call read_wavelength

    @property
    def optical_power(self):
        return self.read_optical_power()  # Automatically call read_optical_power

    @property
    def optical_power_mw(self):
        """
        Converts optical power from dBm to mW.
        Returns:
            float: Optical power in mW.
        """
        optical_power_dbm = self.optical_power  # Use existing optical_power property
        return 10 ** (optical_power_dbm / 10)

    def set_wavelength(self, wavelength):
        if wavelength < 1530:
            wavelength = 1530
        elif wavelength > 1610:
            wavelength = 1610
        self.gpib.query(f"WA{wavelength:.2f}\n")
        self.wait_for_busy()

    def set_power_dbm(self, power):
        self.gpib.query(f"OP{power:.2f}\n")
        self.wait_for_busy()

    def set_power_mw(self, power):
        power_dbm = 10 * math.log10(power)
        self.set_power_dbm(power_dbm)

    def LD_on(self):
        self.gpib.query("LO\n")

    def LD_off(self):
        self.gpib.query("LF\n")

    def read_current(self):
        self.gpib.query("CU\n")
        code = self.gpib.read()
        return float(code)

    def read_LD_temperature(self):
        self.gpib.query("TL\n")
        code = self.gpib.read()
        return float(code)

    def read_wavelength(self):
        self.gpib.query("WA\n")
        code = self.gpib.read()
        self._wavelength = float(code)  # Update private attribute
        return self._wavelength

    def read_optical_power(self):
        self.gpib.query("OP\n")
        code = self.gpib.read()
        self._optical_power = float(code)  # Update private attribute
        return self._optical_power

    def read_coherence_control_value(self):
        self.gpib.query("CV\n")
        code = self.gpib.read()
        return float(code)

    def read_fine_tuning(self):
        self.gpib.query("FT\n")
        code = self.gpib.read()
        return float(code)

    def read_att(self):
        self.gpib.query("AT\n")
        code = self.gpib.read()
        return float(code)

    def check_busy(self):
        su_code = self.su_code
        return su_code[6] != "0"

    def wait_for_busy(self, timeout=100):
        import time

        start_time = time.time()
        while self.check_busy():
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                raise TimeoutError(
                    "Timeout: The operation remained busy for more than the specified timeout."
                )
            time.sleep(0.05)

    def fine_tuning_on(self):
        self.gpib.query("CD\n")
        self.wait_for_busy()

    def fine_tuning_off(self):
        self.gpib.query("CE\n")
        self.wait_for_busy()

    def fine_tuning(self, value):
        if not (-100.00 <= value <= 100.00):
            raise ValueError("Allowed fine tuning value: XXX.XX in range +-100")
        self.gpib.query(f"FT{value:.2f}\n")
        self.wait_for_busy()

    @property
    def fine_tuning_value(self):
        """
        Property to get the current fine tuning value.
        Returns:
            float: The current fine tuning value.
        """
        return self.read_fine_tuning()

    def read_fine_tuning_value(self):
        self.gpib.query("FT\n")
        code = self.gpib.read()
        return float(code)

    @staticmethod
    def visadevlist():
        """
        Static method to list all VISA devices.
        Returns:
            list: A list of available VISA resource names.
        """
        rm = pyvisa.ResourceManager()
        return rm.list_resources()


# Entry point for the project
if __name__ == "__main__":
    print("Initializing Santec Laser Communication...")
    # Example usage of visadevlist
    print("Available VISA devices:", SantecLaser.visadevlist())
    # Add code to initialize and test communication with the laser here.
