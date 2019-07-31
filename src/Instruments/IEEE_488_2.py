# Implements common commands specified in IEEE 488.2

from PyVisaDriver import PyVisaDriver


class IEEE_488_2(PyVisaDriver):

    def __init__(self):
        PyVisaDriver.__init__(self)
        self.name += " that can communicate using IEEE 488.2 common commands - "

    def identify(self):
        """
        Identifies itself using IDN query
        :return:
        """
        if self.check_connected():
            identity = self.device.query("*IDN?")
            return identity
        else:
            raise Exception('Serial communication port is not open.')

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
