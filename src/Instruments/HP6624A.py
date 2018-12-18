# import serial
# import visa
import inspect
import re

import pyvisa


class HP6624A(object):
	methods = []

	def __init__(self, device):
		self.active = False

		self.device = device
		self.run_set_voltage(0, 1)
		self.run_set_voltage(0, 2)
		self.run_set_voltage(0, 3)
		self.run_set_voltage(0, 4)
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.device.close()
		pass

	def who_am_i(self):
		if self.check_connected():
			return "HP6624A at " + self.device.resource_info[0].alias
		else:
			return "HP6624A DISCONNECTED"

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def what_can_i(self):
		if len(HP6624A.methods) == 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					HP6624A.methods.append(method)
		return HP6624A.methods

	def run_change_state(self):
		# if self.active == True:
		# 	self.active = False
		# else:
		# 	self.active = True
		self.active = not self.active

	def run_set_voltage(self, value=0, channel=1):
		"""
		Set the voltage
		:param value: Specified voltage to set channel to
		:type value: Integer
		:param channel: Specified channel to set
		:type channel: Integer
		"""
		self.device.write('VSET ' + str(channel) + ',' + str(value))

	def run_set_current(self, value=0, channel=1):
		"""
		Set the current
		:param value: Specified current to set channel to
		:type value: Integer
		:param channel: Specified channel to set
		:type channel: Integer
		"""
		self.device.write('ISET ' + str(channel) + ',' + str(value))

	def run_set_over_voltage(self, value=0, channel=1):
		"""
		Set the over-voltage

		:param value: Specified over-voltage to set channel to
		:type value: Integer
		:param channel: Specified channel to set
		:type channel: Integer
		"""
		self.device.write('OVSET ' + str(channel) + ',' + str(value))

	def run_set_OC_switch(self, value=0, channel=1):
		"""
		Set the OC Switch

		:param value: Specified value to set channel to
		:type value: Integer
		:param channel: Specified channel to set
		:type channel: Integer
		"""
		self.device.write('OCP ' + str(channel) + ',' + str(value))

	def run_set_output_switch(self, value=0, channel=1):
		"""
		Set the output Switch

		:param value: Specified output value to set channel to
		:type value: Integer
		:param channel: Specified channel to set
		:type channel: Integer
		"""
		self.device.write('OUT ' + str(channel) + ',' + str(value))

	def run_get_set_voltage(self, channel=1):
		"""
		Queries the voltage of a specified channel

		:param channel: Specified channel to query
		:type channel: Integer
		:returns: Integer
		"""
		# self.gpib.write('VSET? ' + str(channel))
		# return self.gpib.read()
		return self.device.query('VSET? ' + str(channel))

	def run_get_set_current(self, channel=1):
		"""
		Queries the current of a specified channel

		:param channel: Specified channel to query
		:type channel: Integer
		:returns: Integer
		"""
		# self.gpib.write('ISET? ' + str(channel))
		# return self.gpib.read()
		return self.device('ISET? ' + str(channel))

	def run_get_out_voltage(self, channel=1):
		"""
		Queries the voltage of a specified channel

		:param channel: Specified channel to query
		:type channel: Integer
		:returns: Integer
		"""
		# self.gpib.write('VOUT? ' + str(channel))
		# return self.gpib.read()
		return self.device.query('VOUT? ' + str(channel))

	def run_get_out_current(self, channel=1):
		"""
		Queries the out-current of a specified channel

		:param channel: Specified channel to query
		:type channel: Integer
		:returns: Integer
		"""
		# self.gpib.write('IOUT? ' + str(channel))
		# return self.gpib.read()
		return self.device.query('IOUT? ' + str(channel))

	def run_get_OC_switch(self, channel=1):
		"""
		Queries the OC switch of a specified channel

		:param channel: Specified channel to query
		:type channel: Integer
		:returns: Integer
		"""
		# self.gpib.write('OCP? ' + str(channel))
		# return self.gpib.read()
		return self.device.query('OCP? ' + str(channel))

	def run_get_out_switch(self, channel=1):
		"""
		Queries the out switch of a specified channel

		:param channel: Specified channel to query
		:type channel: Integer
		:returns: Integer
		"""
		# self.gpib.write('OUT? ' + str(channel))
		# return self.gpib.read()
		return self.device.query('OUT? ' + str(channel))

	def run_save_state(self, mem=1):
		"""
		Stores state within non-volatile memory

		:param mem: Specified space to write to
		:type mem: Integer
		"""
		self.device.write('STO ' + str(mem))

	def run_recall_state(self, mem=1):
		"""
		Loads stored state from specified memory location

		:param mem: Specified space to query
		:type mem: Integer
		"""
		self.device.write('RCL ' + str(mem))
