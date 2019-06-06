import time

from src.Instruments.PyVisaDriver import PyVisaDriver


class PM500(PyVisaDriver):
    """
    This class models a Newport PM500
    """

    def __init__(self, device):
        PyVisaDriver.__init__(self, device, "Newport PM500")
        self.device = device
        self.velocity = 0

    def run_set_velocity(self, velocity):
        self.velocity = velocity

    def run_move_up(self):
        if self.velocity <= 0:
            return
        if self.device.write('YS ' + str(self.velocity))[1] != 0:
            return
        while self.device.query('YSTAT') != 'YL':
            time.sleep(0.01)

    def run_move_dev(self):
        if self.velocity <= 0:
            return
        if self.device.write('YS -' + str(self.velocity))[1] != 0:
            return

        while self.device.query('YSTAT') != 'YL':
            time.sleep(0.01)
