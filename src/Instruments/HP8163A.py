import inspect
import re
import struct

import pyvisa
import visa


class HP8163A(object):
	methods = []

	def __init__(self, device):
		self.device = device
		self.__channel = None
		self.__port = None
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.device.close()
		pass

	def who_am_i(self):
		if self.check_connected():
			return "Agilent 8163A/B at " + self.device.resource_info[0].alias
		else:
			return "Agilent 8163A/B DISCONNECTED"

	def what_can_i(self):
		if len(HP8163A.methods) == 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					HP8163A.methods.append(method)
		return HP8163A.methods

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def run_set_channel(self, channel):
		if '.' in str(channel):
			segments = channel.split('.')
			self.__channel = int(segments[0])
			self.__port = int(segments[1])
		else:
			self.__channel = int(channel)
			self.__port = 1

	def run_get_power(self):
		cmd = 'read'
		cmd += self.__channel + ':chan' + self.__port
		cmd += ':pow?'
		return float(self.device.query(cmd))

	def run_config_meter(self, range):
		if self.__port != 2:
			range = str(range)
			self.device.write('sens' + self.__channel + ':chan' + self.__port + ':pow:unit 0')
			self.device.write('sens' + self.__channel + ':chan' + self.__port + ':pow:range:auto 0')
			self.device.write('sens' + self.__channel + ':chan' + self.__port + ':pow:range ' + range + 'DBM')

	def run_prep_measure_on_trigger(self, samples=64):
		if self.__port != 2:
			self.device.write('*CLS')
			samples = str(samples)
			self.device.write('sens' + self.__channel + ':chan' + self.__port + ':func:stat logg,stop')
			self.device.write('trig' + self.__channel + ':chan' + self.__port + ':inp sme')
			self.device.query('trig' + self.__channel + ':inp?')
			self.device.write('sens' + self.__channel + ':chan' + self.__port + ':func:par:logg ' + samples + ',100us')
			self.device.query('sens' + self.__channel + ':chan' + self.__port + ':func:par:logg?')
			self.device.write('sens' + self.__channel + ':chan' + self.__port + ':func:stat logg,start')
			self.device.query('sens' + self.__channel + ':chan' + self.__port + ':func:stat?')
			self.device.query('syst:err?')

	def run_get_results_from_log(self, samples=64):
		if self.__port != 2:
			self.device.query('sens' + self.__channel + ':chan' + self.__port + ':func:stat?')
		samples = int(samples)
		self.device.write('sens' + self.__channel + ':chan' + self.__port + ':func:res?')
		raw_data = self.device.read_raw()
		self.device.query('syst:err?')

		num_digits = int(raw_data[1])
		hex_data = raw_data[2 + num_digits: 2 + num_digits + samples * 4]
		flo_data = []

		for idx in range(0, samples*4-1,4):
			data = hex_data[idx: idx+4]
			value = struct.unpack('<f', struct.pack('4c', *data))[0]
			flo_data.append(value)

		return flo_data[1:]
