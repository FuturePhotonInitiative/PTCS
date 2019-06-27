from src.Instruments.PyVisaDriver import PyVisaDriver

TERM_STRING_MAP = ["\r\n", "\r", "\n", ""]


# settings for the device are stored in non-volatile memory

# WARNING: all commands sent through this adapter to an instrument
# should escape all '+' characters with an ESC ASCII character
class GPIBtoUSBAdapter(PyVisaDriver):

    def __init__(self):
        PyVisaDriver.__init__(self)
        self.name += " that is connected using a GPIB to USB Adapter - "

    def get_gpib_termination_string(self):
        """
        :return: the termination characters that will be added to every message sent to the instrument
        """
        return TERM_STRING_MAP[int(self.device.query("++eos")[0])]

    def set_gpib_termination_string(self, term_string):
        """
        sets the termination characters that will be added to every message sent to the instrument
        :param term_string: should be one of four choices (given in the above static list)
        """
        self.device.write("++eos " + str(TERM_STRING_MAP.index(term_string)))

    def query_gpib_address(self):
        """
        :return: the GPIB address the adapter is set to interact with if in Controller mode. Make sure this matches the
        instrument's GPIB address or the adapter will fail to send commands correctly
        """
        return int(self.device.query("++addr"))

    def set_gpib_address(self, address):
        """
        :param address: the GPIB address to make the adapter talk to
        """
        self.device.write("++addr " + str(address))

    def become_controller_in_charge(self):
        self.device.write("++ifc")

    def _query_current_mode(self):
        """
        :return: 1 if in controller mode, 0 if in device mode
        """
        return self.device.query("++mode")

    def i_am_controller(self):
        return self._query_current_mode() == "1"

    def i_am_device(self):
        return self._query_current_mode() == "0"

    def become_controller(self):
        self.device.write("++mode 1")

    def become_device(self):
        self.device.write("++mode 0")

    def reset_adapter_factory_settings(self):
        self.device.write("++rst")

    def unlock_screen(self):
        """
        Sometimes the screen locks when controlling the device and does not shut off when you are done.
        This can be called to shut it off when you are done
        """
        self.device.write("++loc")

    def lock_screen(self):
        """
        Not sure why this is used but it is here anyway. All the instruments i used lock the screen automatically
        """
        self.device.write("++llo")

    def read(self):
        """
        :return: the string sent from the instrument before EOI is asserted
        """
        return self.device.query("++read eoi")

    def query_autoread_status(self):
        """
        :return: 1 for read-after-write, 0 for just write
        """
        return self.device.query("++auto")

    def turn_off_read_after_write(self):
        """
        do not have the adapter listen for a response automatically after sending a command
        """
        self.device.write("++auto 0")

    def turn_on_read_after_write(self):
        """
        have the adapter listen for a response automatically after sending a command
        """
        self.device.write("++auto 1")
