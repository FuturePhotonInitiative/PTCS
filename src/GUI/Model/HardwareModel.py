class HardwareModel:
    """
    Class which represents the configuration of a hardware device
    """
    def __init__(self, name, driver, connection_type, default_connection):
        self.name = name
        self.driver = driver
        self.connection_type = connection_type
        self.default_connection = default_connection
