from src.Instruments.PyVisaDriver import PyVisaDriver

TERM_STRING_MAP = ["\r\n", "\r", "\n", ""]


# settings for the device are stored in non-volatile memory

# WARNING: all commands sent through this adapter to an instrument
# should escape all '+' characters with an ESC ASCII character

# all of these methods are private because a user using the GUI should not need to call these directly
class GPIBtoUSBAdapter(PyVisaDriver):
    """
    This is the class that drives the yellow GPIB to USB adapter owned by the CFD.
    https://www.sparkfun.com/products/549

    Underscored method names usually indicate that only that class should use those methods, but in this case
    it means that the user building a test on the test build page should not need to think about using these
    methods, and therefore wont be shown to pick from on the UI.

    Devices that extend this class may use them though.
    """

    def __init__(self):
        # the GPIB address the instrument extending this class is set to
        self.instrument_gpib_address = None

        PyVisaDriver.__init__(self)
        self.name += " that is connected using a GPIB to USB Adapter - "

    def _get_gpib_termination_string(self):
        """
        :return: the termination characters that will be added to every message sent to the instrument
        """
        return TERM_STRING_MAP[int(self.device.query("++eos")[0])]

    def _set_gpib_termination_string(self, term_string):
        """
        sets the termination characters that will be added to every message sent to the instrument
        :param term_string: should be one of four choices (given in the above static list)
        """
        self.device.write("++eos " + str(TERM_STRING_MAP.index(term_string)))

    def _get_gpib_address(self):
        """
        :return: the GPIB address the adapter is set to interact with if in Controller mode. Make sure this matches the
        instrument's GPIB address or the adapter will fail to send commands correctly
        """
        return int(self.device.query("++addr"))

    def _communicate_using_my_gpib_address(self):
        """
        Set the adapter to listen to the gpib address that the device extending this class is set to
        """
        self.device.write("++addr {}".format(self.instrument_gpib_address))

    def _become_controller_in_charge(self):
        self.device.write("++ifc")

    def _query_current_mode(self):
        """
        :return: 1 if in controller mode, 0 if in device mode
        """
        return self.device.query("++mode")

    def _i_am_controller(self):
        return self._query_current_mode() == "1"

    def _i_am_device(self):
        return self._query_current_mode() == "0"

    def _become_controller(self):
        self.device.write("++mode 1")

    def _become_device(self):
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

    def _gpib_read(self):
        """
        send a read command to the GPIB connected instrument and read the data before EOI is asserted or timeout
        """
        self._communicate_using_my_gpib_address()
        return self.device.query("++read eoi")

    def _get_autoread_status(self):
        """
        :return: 1 for read-after-write, 0 for just write
        """
        return self.device.query("++auto")

    def _turn_off_read_after_write(self):
        """
        do not have the adapter listen for a response automatically after sending a command
        """
        self.device.write("++auto 0")

    def _turn_on_read_after_write(self):
        """
        have the adapter listen for a response automatically after sending a command
        """
        self.device.write("++auto 1")

    def _query_device(self, query, termination=""):
        """
        The GPIB to USB adapter needs to know that it is expecting a response from the instrument.
        :param query: the query string to ask the instrument
        :param termination: the character string to end the message with
        :return: the response string
        """
        if self._get_gpib_address() != self.instrument_gpib_address:
            self._communicate_using_my_gpib_address()
        self._turn_on_read_after_write()
        return self.device.query(query + termination)

    def _send_to_device(self, query, termination=""):
        """
        :param query: the query string to ask the instrument
        :param termination: the character string to end the message with
        """
        if self._get_gpib_address() != self.instrument_gpib_address:
            self._communicate_using_my_gpib_address()
        self._turn_off_read_after_write()
        self.device.write(query + termination)
