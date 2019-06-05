# Class for Agilent 33401A Power Supply
"""
MODIFICATION HISTORY:
	6/11/2018
	Adds def get_feedback(self) method
"""

import pyvisa
import inspect
import re


class Agilent34401A(object):
	"""
	This class models the Agilent 34401A Power Supply.
	"""

	methods = []

	def __init__(self, device, scaling_factor=1):
		"""
		Constructor method
		standard address='GPIB::22::INSTR'
		"""
		self.device = device
		self.scaling_factor = scaling_factor

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

	def what_can_i(self):
		if len(Agilent34401A.methods) is 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					Agilent34401A.methods.append(method)
		return Agilent34401A.methods

	def who_am_i(self):
		"""
		:returns: reference to device
		"""
		if self.check_connected():
			return "Agilent 33401A at " + self.device.resource_info[0].alias
		else:
			return "Agilent 33401A DISCONNECTED"

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def run_get_voltage(self, scaled=False, query_range=10, resolution=0.01):
		"""
		Queries the voltage of multimeter.

		:param scaled: Optional scaling
		:type scaled: Boolean
		:param query_range: range for query
		:type query_range: Integer
		:param resolution: resolution for query
		:type resolution: Float
		:returns: current voltage reading as float
		"""

		try:
			val = float(self.device.query('MEAS:VOLT:DC? '+str(query_range)+','+str(resolution)))
			if scaled is True:
				val = val*self.scaling_factor
			return val
		except pyvisa.errors.VisaIOError:
			return False

	def run_get_current(self, query_range=1, resolution=0.000001):
		"""
		Queries the current reading of the multimeter

		:param query_range: range for query
		:type query_range: Integer
		:param resolution: resolution for query
		:type resolution: Float
		:returns: current reading as float
		"""
		try:
			return float(self.device.query('MEAS:CURR:DC? '+str(query_range)+','+str(resolution)))
		except pyvisa.errors.VisaIOError:
			return False

	def run_get_feedback(self):
		"""
		Requirement for generic feedback
		"""
		return self.run_get_current()

	def run_set_scaling(self, factor=1):
		"""
		Sets the scaling factor of the multimeter instrument.

		:param factor: Desired factor
		:type factor: Float or Integer
		"""

		self.scaling_factor = factor

	def run_get_scaling(self):
		"""
		Gets the scaling factor.

		:returns: Scaling factor as Int or Float
		"""

		return self.scaling_factor


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
