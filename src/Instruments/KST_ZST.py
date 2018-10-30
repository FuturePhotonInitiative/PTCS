import re
import inspect
import sys
import time
from struct import unpack

import pyvisa


class Motor_KST_ZST(object):
	methods = []

	def __init__(self, device):
		self.device = device
		self.device.values_format.is_binary = True
		self.device.values_format.datatype = 'd'
		self.device.values_format.is_big_endian = sys.byteorder == 'little'
		self.device.values_format.container = bytearray

		self.position = 0
		self.zeros_position = 0
		self._steps = 0
		pass

	def __enter__(self):
		return self.device

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.device.close()
		return

	def who_am_i(self):
		if self.check_connected():
			return "KST_Z812B at " + self.device.resource_info[0].alias
		else:
			return "KST_Z812B DISCONNECTED"

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def what_can_i(self):
		if len(Motor_KST_ZST.methods) == 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					Motor_KST_ZST.methods.append(method)
		return Motor_KST_ZST.methods

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
