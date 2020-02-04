class HardwareModel:
    """
    Class which represents the configuration of a hardware device
    """
    def __init__(self, Driver, Type, Default):
        self.driver = Driver
        self.type = Type
        self.default = Default
