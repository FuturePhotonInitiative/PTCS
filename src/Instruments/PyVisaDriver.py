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
        if self.device:
            self.device.close()

    def who_am_i(self):
        if self.check_connected():
            return self.name + " - Connected to " + self.device.resource_info[0].alias
        else:
            return self.name + " DISCONNECTED"

    def check_connected(self):
        """
        Every implementing class should reimplement this method. This will be called to query the instrument to see if
        the instrument will return back a known value. If the connection times out, we know the instrument is really
        not connected.
        :return: true if PyVisa interacted with an intermediary adapter, false if this object was not established correctly.
        """
        if not self.device:
            return False
        try:
            return self.device.session is not None
        except pyvisa.errors.InvalidSession:
            self.device = None
            return False
