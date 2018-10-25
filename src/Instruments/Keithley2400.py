import re
import inspect
import pyvisa


class Keithley2400(object):
	methods = []

	def __init__(self, device):
		self.device = device
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.device.close()
		pass

	def who_am_i(self):
		if self.check_connected():
			return "Keithley 2400 at " + self.device.resource_info[0].alias
		else:
			return "Keithley 2400 DISCONNECTED"

	def what_can_i(self):
		if len(Keithley2400.methods) == 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					Keithley2400.methods.append(method)
		return Keithley2400.methods

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def run_get_voltage(self, query_range=10, resolution=0.01):
		query_range = str(query_range)
		resolution = str(resolution)
		return float(self.device.query(':MEAS:VOLT:DC?' + query_range + ',' + resolution))

	def run_get_current(self, query_range=1, resolution=0.000001):
		query_range = str(query_range)
		resolution = str(resolution)
		return float(self.device.query(':MEAS:CURR:DC?' + query_range + ',' + resolution))

	def run_set_voltage(self, voltage=0):
		self.device.write(':SOUR:FUNC VOLT')
		self.device.write(':SOUR:VOLT ' + str(voltage))

	def run_set_current(self, current=0):
		self.device.write(':SOUR:FUNC CURR')
		self.device.write(':SOUR:CURR ' + str(current))

	def run_set_over_voltage(self, voltage=0):
		self.device.write(':SENS:VOLT:PROT ' + str(voltage))

	def run_set_over_current(self, current=0):
		self.device.write(':SENS:CURR:PROT ' + str(current))

	def run_set_output_switch(self, state=False):
		self.device.write(':OUTP ' + 'ON' if state else 'OFF')

	def run_get_set_voltage(self):
		return self.device.query(':SOUR:VOLT?')

	def run_get_set_current(self):
		return self.device.query(':SOUR:CURR?')

	def run_get_output_switch(self):
		return self.device.query(':OUTP?')

	def run_save_state(self, slot=1):
		self.device.write('*SAV ' + str(slot))

	def run_recall_state(self, slot=1):
		self.device.write('*RCL ' + str(slot))
