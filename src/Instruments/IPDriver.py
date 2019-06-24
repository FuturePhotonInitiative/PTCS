from src.Instruments.EVTDriver import EVTDriver


class IPDriver(EVTDriver):

    def __init__(self, IP):
        self.IP = IP
        EVTDriver.__init__(self)
        self.name += "A device that does not use PyVisa to connect: " + self.name

    def __enter__(self):
        """
        Enter method for ability to use "with open" statements
        :return: Driver Object
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def who_am_i(self):
        if self.check_connected():
            return self.name + " - at IP: " + self.IP
        else:
            return self.name + " DISCONNECTED"

    def check_connected(self):
        return self.device.IsOnline()[0]
