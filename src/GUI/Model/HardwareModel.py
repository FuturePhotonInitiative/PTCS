class HardwareModel:
    """
    Class which represents the configuration of a hardware device
    """
    def __init__(self, Driver, Type, Default):
        self.driver = Driver
        self.type = Type
        self.default = Default

    def uses_pyvisa(self):
        """
        If this does not use pyVISA, it is probably connected using an IP address, so self.type == "DIRECT"
        :return:
        """
        return self.type == "VISA"
