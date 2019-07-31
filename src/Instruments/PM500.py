import time

from src.Instruments.PyVisaDriver import PyVisaDriver


class PM500(PyVisaDriver):
    """
    This class models a Newport PM500
    """

    def __init__(self, device):
        PyVisaDriver.__init__(self)
        self.name += "Newport PM500"
        self.device = device
        self.velocity = 0

    def set_velocity(self, velocity):
        self.velocity = velocity

    def move_up(self):
        if self.velocity <= 0:
            return
        if self.device.write('YS ' + str(self.velocity))[1] != 0:
            return
        while self.device.query('YSTAT') != 'YL':
            time.sleep(0.01)

    def move_dev(self):
        if self.velocity <= 0:
            return
        if self.device.write('YS -' + str(self.velocity))[1] != 0:
            return

        while self.device.query('YSTAT') != 'YL':
            time.sleep(0.01)
