from .PyVisaDriver import PyVisaDriver


class IEEE_488_2(PyVisaDriver):
    """
    Implements common commands specified in IEEE 488.2
    """

    def __init__(self):
        PyVisaDriver.__init__(self)
        self.name += " that can communicate using IEEE 488.2 common commands - "

    def check_connected(self):
        """
        Use the IEEE 488.2 defined *IDN? query to see if the instrument is actually connected.
        :return: If it is actually connected, it will return a value, so return True. If not, it will timeout and raise an exception, so return False.
        """
        try:
            identity = self.device.query("*IDN?")
            return True
        except Exception:
            return False

    def reset(self):
        """
        Restores the majority of the instrument's settings to their default values
        """
        self.device.write("*RST")

    def clear_status(self):
        """
        clear status command. If an error message is currently posted on the test set's display,
        this command also closes the error message.
        """
        self.device.write('*CLS')
