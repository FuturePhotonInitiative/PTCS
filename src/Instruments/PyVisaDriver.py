from src.Instruments.EVTDriver import EVTDriver
import pyvisa


class PyVisaDriver(EVTDriver):
    """
    An abstract class that will be extended by an instrument driver
    that needs to use PyVISA for instrument connection
    """

    def __init__(self):
        EVTDriver.__init__(self)
        if "PyVisa" not in self.name:
            self.name = "A PyVisa Driver "

    def __enter__(self):
        """
        Enter method for ability to use "with open" statements
        :return: Driver Object
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the device connection
        """
        self.device.close()

    def who_am_i(self):
        if self.check_connected():
            return self.name + " - Connected to " + self.device.resource_info[0].alias
        else:
            return self.name + " DISCONNECTED"

    def check_connected(self):
        if not self.device:
            return False
        try:
            return self.device.session is not None
        except pyvisa.errors.InvalidSession:
            self.device = None
            return False
