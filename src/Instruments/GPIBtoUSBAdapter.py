from src.Instruments.PyVisaDriver import PyVisaDriver

TERM_STRING_MAP = ["\r\n", "\r", "\n", ""]


# settings for the device are stored in non-volatile memory

# WARNING: all commands sent through this adapter to an instrument
# should escape all '+' characters with an ESC ASCII character
class GPIBtoUSBAdapter(PyVisaDriver):

    def __init__(self):
        PyVisaDriver.__init__(self)
        self.name += " that is connected using a GPIB to USB Adapter - "

    def query_usb_send_eos_state(self):
        return TERM_STRING_MAP[int(self.device.query("++eos")[0])]

    def set_usb_send_eos_state(self, term_string):
        self.device.write("++eos " + str(TERM_STRING_MAP.index(term_string)))

    def query_gpib_address(self):
        return self.device.query("++addr")

    def set_gpib_address(self, address):
        self.device.write("++addr " + str(address))

    def become_controller_in_charge(self):
        self.device.write("++ifc")

    def query_current_mode(self):
        return self.device.query("++mode")

    def become_controller(self):
        self.device.write("++mode 1")

    def become_device(self):
        self.device.write("++mode 0")

    def reset_usb_gpib_controller_factory_settings(self):
        self.device.write("++rst")

    def read(self):
        return self.device.query("++read eoi")

    def query_autoread_status(self):
        return self.device.query("++auto")

    def turn_off_read_after_write(self):
        self.device.write("++auto 0")

    def turn_on_read_after_write(self):
        self.device.write("++auto 1")
