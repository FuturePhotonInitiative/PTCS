import time

import pyvisa
import re
import inspect


class Keithley2280S(object):
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
			return "Keithley 2280S at " + self.device.resource_info[0].alias
		else:
			return "Keithley 2280S DISCONNECTED"

	def what_can_i(self):
		if len(Keithley2280S.methods) == 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					Keithley2280S.methods.append(method)
		return Keithley2280S.methods

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def run_get_voltage(self, channel=1):
		channel = str(channel)
		self.device.write(':SENS' + channel + ':FUNC "VOLT')
		self.device.write(':TRAC:CLE')
		time.sleep(0.3)
		return float(self.device.query(':DATA' + channel + ':DATA? "READ,UNIT"').split(',')[0][:-1])

	def run_get_current(self, channel=1):
		channel = str(channel)
		self.device.write(':SENS' + channel + ':FUNC "CURR"')
		self.device.write(':TRAC:CLE')
		time.sleep(0.3)
		return float(self.device.query('DATA' + channel + ':DATA? "READ,UNIT"').split(',')[0][:-1])

	def run_set_voltage(self, voltage=0, channel=1):
		voltage = str(voltage)
		channel = str(channel)
		self.device.write(':SOUR' + channel + ':VOLT ' + voltage)

	def run_set_current(self, current=0, channel=1):
		current = str(current)
		channel = str(channel)
		self.device.write(':SOUR' + channel + ':CURR ' + current)

	def run_set_over_voltage(self, voltage=0, channel=1):
		voltage = str(voltage)
		channel = str(channel)
		self.device.write(':SOUR' + channel + ':VOLT:PROT ' + voltage)

	def run_set_over_current(self, current=0, channel=1):
		current = str(current)
		channel = str(channel)
		self.device.write(':SOUR' + channel + ':CURR:PROT ' + current)

	def run_set_output_switch(self, value=0, channel='CH1'):
		value = str(value)
		channel = str(channel)
		self.device.write('OUTP ' + value + ',' + channel)

	def run_get_set_voltage(self, channel=1):
		channel = str(channel)
		return self.device.query(':SOUR' + channel + ':VOLT?')

	def run_get_set_current(self, channel=1):
		channel = str(channel)
		return self.device.query(':SOUR' + channel + ':CURR?')

	def run_get_out_switch(self):
		return self.device.query('OUTP?')

	def run_save_state(self, slot=1):
		self.device.write('*SAV ' + str(slot))

	def run_recall_state(self, slot=1):
		self.device.write('*RCL ' + str(slot))
