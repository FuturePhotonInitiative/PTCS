import sys
import time
from struct import unpack

from src.Instruments.PyVisaDriver import PyVisaDriver


class Motor_KST_ZST(PyVisaDriver):

    def __init__(self, device):
        PyVisaDriver.__init__(self)
        self.name += "KST_Z812B"
        self.device = device

        self.device.values_format.is_binary = True
        self.device.values_format.datatype = 'd'
        self.device.values_format.is_big_endian = sys.byteorder == 'little'
        self.device.values_format.container = bytearray

        self.position = 0
        self.zeros_position = 0
        self._steps = 0

    def run_delta_move(self, steps):
        self.position += steps

        self.device.write_raw([0x48, 0x04, 0x06, 0x00, 0xD0, 0x01])
        self.device.write_raw([0x01, 0x00])
        self.device.write_binary_values('', [steps], datatype='i', is_big_endian=sys.byteorder != 'little')
        self.__move_complete__()

    def run_abs_move(self, steps):
        self.device.write_raw([0x48, 0x04, 0x06, 0x00, 0xD0, 0x01])
        self.device.write_raw([0x01, 0x00])
        self.device.write_binary_values('', [steps - self.position], datatype='i', is_big_endian=sys.byteorder != 'little')
        self.position = steps
        self.__move_complete__()

    def run_get_position(self):
        return self.position

    def run_set_as_zero(self, new_zero):
        self.zeros_position = new_zero
        self.position -= new_zero

    def run_set_vel_params(self, initial_velocity, acceleration, final_velocity):
        self.device.write_raw([0x13, 0x04, 0x0E, 0x00, 0xD0, 0x01])
        self.device.write_raw([0x01, 0x00])
        self.device.write_binary_values('', [initial_velocity], datatype='i', is_big_endian=sys.byteorder != 'little')
        self.device.write_binary_values('', [acceleration], datatype='i', is_big_endian=sys.byteorder != 'little')
        self.device.write_binary_values('', [final_velocity], datatype='i', is_big_endian=sys.byteorder != 'little')

    def __str__(self):
        return 'position: ' + str(self.position) + '\nzeros-position: ' + str(self.zeros_position)

    def __move_complete__(self):
        while self.device.bytes_in_buffer != 0:
            self.device.read_bytes(1)
            time.sleep(0.01)

        while self.device.bytes_in_buffer == 0:
            time.sleep(0.1)

        response = self.device.read_bytes(2)
        while response != [0x64, 0x04]:
            while self.device.bytes_in_buffer == 0:
                time.sleep(0.1)
            response = self.device.read_bytes(2)

        rest = self.device.read_bytes(18)
        self._steps = unpack('<l', rest[6:10])[0]

    def __get_count__(self):
        return self._steps

    def __go_to_abs__(self, steps):
        self.device.write_raw([0x53, 0x04, 0x06, 0x00, 0xD0, 0x01])
        self.device.write_raw([0x01, 0x00])
        self.device.write_binary_values('', [steps], datatype='i', is_big_endian=sys.byteorder != 'little')
        self.position = steps
        self.__move_complete__()
