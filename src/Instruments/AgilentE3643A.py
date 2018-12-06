# Class for Agilent E3643A DC Power Supply

import inspect
import re
import time
import pyvisa
import pyvisa.constants


class AgilentE3643A(object):
	"""
	This class models the Agilent DC power supply.
	"""

	methods = []

	def __init__(self, device):
		"""
		Constructor method.

		:param device: device from PyVisa open_resource object
		:type: PyVisa open_resource object
		"""
		self.device = device

	def __enter__(self):
		"""
		Enter method for ability to use "with open" statements
		:return: Driver Object
		"""
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		"""
		Exit to close object
		:param exc_type:
		:param exc_val:
		:param exc_tb:
		:return:
		"""
		self.device.close()
		pass

	def who_am_i(self):
		if self.check_connected():
			return "Agilent E3643A at " + self.device.resource_info[0].alias
		else:
			return "Agilent E3643A DISCONNECTED"

	def what_can_i(self):
		if len(AgilentE3643A.methods) is 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					AgilentE3643A.methods.append(method)
		return AgilentE3643A.methods

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def run_identify(self):
		"""
		Identifies itself using IDN query
		:return:
		"""
		if self.check_connected():
			identity = self.device.query("*IDN?")
			return identity
		else:
			raise Exception('Serial communication port is not open.')

	def run_get_voltage(self):
		"""
		Gets the voltage.
		:return: the measured DC voltage
		:raises: Exception when serial communication port is not open
		"""
		if self.check_connected():
			voltage = self.device.query("MEAS:VOLT:DC?")
			return voltage
		else:
			raise Exception('Serial communication port is not open.')

	def run_get_current(self):
		"""Gets the current.
		:return: the measured DC current
		:raises: Exception when serial communication port is not open
		"""
		if self.check_connected():
			current = self.device.query('MEAS:CURR:DC?')
			return float(current)
		else:
			raise Exception('Serial communication port is not open.')

	def run_set_voltage(self, value=0):
		"""
		Sets the voltage.

		:param value: Specified voltage value, defaults to 0
		:type value: float
		:raises: Exception when serial communication port is not open
		"""
		if self.check_connected():
			self.device.write('VOLT {}'.format(str(value)))
			time.sleep(0.25)
		else:
			raise Exception('Serial communication port is not open.')

	def run_set_current(self, value=0):
		"""
		Sets the current.

		:param value: Specified current value, defaults to 0
		:type value: float
		:raises: Exception when serial communication port is not open
		"""
		if self.check_connected():
			self.device.write('CURR {}'.format(str(value)))
			time.sleep(0.25)
		else:
			raise Exception('Serial communication port is not open.')

	def run_set_over_voltage(self, value=0):
		"""
		Sets the over voltage.

		:param value: Specified voltage value, defaults to 0
		:type value: float
		:raises: Exception when serial communication port is not open
		"""
		if self.check_connected():
			self.device.write('VOLT:PROT {}'.format(str(value)))
			time.sleep(0.25)
		else:
			raise Exception('Serial communication port is not open.')

	def set_output_switch(self, value=0):
		"""
		Set the output switch to 1 -> ON or 0 -> OFF

		:param value: Specified state, defaults to 0 for OFF, 1 for ON
		:type value: Integer
		:raises: Exception when serial communication port is not open or value is not 0 or 1
		"""
		if self.check_connected():
			if value == 0 or value == 1:
				if value == 1:
					self.device.write("OUTP:STAT ON")
				else:
					self.device.write("OUTP:STAT OFF")
				time.sleep(0.25)
			else:
				raise Exception('Input value is incorrect, must be 1 for ON or 0 for OFF')
		else:
			raise Exception('Serial communication port is not open.')

	def run_save_state(self, mem=1):
		"""
		Stores state within non-volatile memory

		:param mem: Specified space to write to
		:type mem: Integer
		"""
		if mem > 5 or mem < 1:
			raise Exception('Invalid memory space: ' + str(mem) + ', valid states are {1,2,3,4,5}')
		if self.check_connected():
			self.device.write('*SAV {}'.format(mem))
			time.sleep(0.25)
		else:
			raise Exception('Serial communication port is not open.')

	def run_recall_state(self, mem=1):
		"""
		Loads stored state from specified memory location

		:param mem: Specified space to query
		:type mem: Integer
		"""
		if mem > 5 or mem < 1:
			raise Exception('Invalid memory space: ' + str(mem) + ', valid states are {1,2,3,4,5}')
		if self.check_connected():
			self.device.write('*RCL {}'.format(mem))
			time.sleep(0.25)
		else:
			raise Exception('Serial communication port is not open.')
