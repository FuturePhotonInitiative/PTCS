import inspect
import re
import pyvisa
from time import sleep


class AEDFA_IL_23_B_FA(object):
	"""
	This class models an Amonics EDFA.
	:warning: Baud rate in device needs to be set to 115200
	"""

	methods = []

	def __init__(self, device):
		"""
		Constructor method for AEDFA instrument
		:param device: PyVisa open_resource object
		"""

		self.device = device

	def __enter__(self):
		"""
		Enter method for ability to use "with open" statements
		:return: Driver Object
		"""
		return self

	def __exit__(self):
		"""
		Exit to close object
		:return:
		"""
		self.device.close()

	def who_am_i(self):
		if self.check_connected():
			return "AEDFA-IL-23-B-FA at " + self.device.resource_info[0].alias
		else:
			return "AEDFA-IL-23-B-FA DISCONNECTED"

	def what_can_i(self):
		if len(AEDFA_IL_23_B_FA.methods) is 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					AEDFA_IL_23_B_FA.methods.append(method)
		return AEDFA_IL_23_B_FA.methods

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def close(self):
		"""
		Closes session with resource
		:return:
		"""

		self.device.close()

	def set_mode(self, mode):
		"""
		Sets the mode for the instrument.
		:param mode: Operating mode for instrument. Possible inputs at -> mode_options()
		:type mode: String
		"""

		self.device.write(":MODE:SW:CH1 "+mode+" \n")

	def run_get_mode(self):
		"""
		Query the current mode of instrument.
		:returns: String, current mode.
		"""

		self.device.write(":MODE:SW:CH1? \n")
		return self._read2cr()

	def run_mode_options(self):
		"""
		Queries available modes for the instrument.
		:returns: String of available modes
		"""

		self.device.write(":READ:MODE:NAMES? \n")
		return self._read2cr()

	def run_set_power(self, power):
		"""
		Set the driving set-point of the specified <mode> for the specified channel
		:param power: specified power
		:type power: Float
		"""

		self.device.write(":DRIV:APC:CUR:CH1 "+str(power)+" \n")

	def run_get_set_power(self):
		"""
		Queries the current set power
		:returns: Float
		"""
		if self.run_get_mode() == "APC":
			self.device.write(":DRIV:APC:CUR:CH1? \n")
			return self._read2cr()
		else:
			return -1

	def run_set_pump_currents(self, channel, current):
		"""
		Sets the specified current for a particular channel.

		:param channel: Specified channel
		:type channel: Integer
		:param current: Specified current
		:type current: Float
		"""

		self.device.write(":DRIV:ACC:CUR:CH"+str(channel)+" "+str(current)+" \n")

	def run_get_pump_currents(self, channel):
		"""
		Queries the current for specified channel.
		:returns: Float
		"""

		if self.run_get_mode() == "ACC":
			self.device.write(":DRIV:ACC:CUR:CH"+str(channel)+"? \n")
			return self._read2cr()
		else:
			return -1

	def run_set_status_pumps(self, state=1):
		"""
		Sets the status for pump.
		:param state: specified state
		:type state: Integer
		"""
		if self.run_get_mode() == "ACC":
			self.device.write(":DRIV:ACC:STAT:CH1 "+str(state)+" \n")
			sleep(0.01)
			self.device.write(":DRIV:ACC:STAT:CH2 "+str(state)+" \n")
		elif self.run_get_mode() == "APC":
			self.device.write(":DRIV:APC:STAT:CH1 "+str(state)+" \n")

	def run_set_master_out(self, state=1):
		"""
		Sets master control switch
		:param state: 1 means ON and 0 means OFF
		:type state: Integer
		"""

		if state == 1:
			self.device.write(":DRIV:MCTRL 1 \n")
		else:
			self.device.write(":DRIV:MCTRL 0 \n")

	def run_get_master_out(self):
		"""
		Get the master control switch status
		:returns: Integer; 0,1,2 for OFF, ON, BUSY respectively
		"""
		self.device.write(":DRIV:MCTRL? \n")
		return self._read2cr()

	def run_get_out_power(self):
		"""
		Get the existing input power value of the specified channel.
		:returns: Float
		"""
		self.device.write(":SENS:POW:OUT:CH1? \n")
		return self._read2cr()

	def _read2cr(self):
		"""
		Internal function for reading instrument
		"""
		sleep(0.01)
		response = ''
		letter = self.device.read()
		while letter != '\n':
			response += letter
			letter = self.device.read()
		return response[0:-1]


'''
Copyright (C) 2017  Robert Polster
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
