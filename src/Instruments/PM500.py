import re
import time
import pyvisa
import inspect


class PM500(object):
	methods = []

	def __init__(self, device):
		self.device = device
		self.velocity = 0
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.device.close()
		pass

	def who_am_i(self):
		if self.check_connected():
			return "Newport PM500 at " + self.device.resource_info[0].alias
		else:
			return "Newport PM500 DISCONNECTED"

	def what_can_i(self):
		if len(PM500.methods) == 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					PM500.methods.append(method)
		return PM500.methods

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def run_set_velocity(self, velocity):
		self.velocity = velocity

	def run_move_up(self):
		if self.velocity <= 0:
			return
		if self.device.write('YS ' + str(self.velocity))[1] != 0:
			return
		while self.device.query('YSTAT') != 'YL':
			time.sleep(0.01)

	def run_move_dev(self):
		if self.velocity <= 0:
			return
		if self.device.write('YS -' + str(self.velocity))[1] != 0:
			return

		while self.device.query('YSTAT') != 'YL':
			time.sleep(0.01)
