import re
import inspect
import pyvisa


class MS2667C(object):
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
			return "Anritsu MS2667C at " + self.device.resource_info[0].alias
		else:
			return "Anritsu MS2667C DISCONNECTED"

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def what_can_i(self):
		if len(MS2667C.methods) == 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					MS2667C.methods.append(method)
		return MS2667C.methods

	def run_waveform_read_central(self, central, span, resolution_step=1):
		self.device.write('CF %dMHZ' % central)
		self.device.write('SP %dMHZ' % span)
		self.device.write('TS')

		self.device.write('BIN 0')

		values = []
		for count in range(0, 500, resolution_step):
			values.append(float(self.device.query('XMA? %d, %d' % (count, resolution_step))))

		return values

	def run_waveform_read_range(self, start, end, resolution_step=1):
		self.device.write('FA %dMHZ' % start)
		self.device.write('FB %dMHZ' % end)
		self.device.write('TS')

		self.device.write('BIN 0')

		values = []

		for count in range(0, 500, resolution_step):
			values.append(float(self.device.query('XMA? %d %d' % (count, resolution_step))))

		return values

	def run_get_peak(self, central, span):
		self.device.write('CF %dMHZ' % central)
		self.device.write('SP %dMHZ' % span)
		self.device.write('TS')

		self.device.write('MKR 0')
		self.device.write('MKPK')
		peak_frequency = float(self.device.query('MKF?'))

		level = float(self.device.query('MKL?'))

		return peak_frequency, level
