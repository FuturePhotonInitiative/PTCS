import re
import inspect
import pyvisa
from KST_ZST import Motor_KST_ZST


class KST_Z812B(Motor_KST_ZST):
	methods = []

	def __init__(self, device):
		super(Motor_KST_ZST, self).__init__(device)
		self.device = device
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.device.close()
		pass

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
		if len(KST_Z812B.methods) is 0:
			KST_Z812B.methods = super(self).what_can_i()
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					for sub_method in KST_Z812B.methods:
						if method[0] is sub_method[0]:
							KST_Z812B.methods.remove(sub_method)
							break
					KST_Z812B.methods.append(method)
		return KST_Z812B.methods

	def run_home(self):
		"""
		Puts the motor to backward limit position so that the
		position markers make sense
		"""

		# variable moving is not necessary
		# self.moving = True
		self.device.write_raw([0x43, 0x04, 0x01, 0x00, 0x50, 0x01])
		response = self.device.read()
		if response != [0x44, 0x04, 0x01, 0x00, 0x01, 0x50]:
			# self.logger.error('problem homing', extra=self.ext)
			# raise error?
			exit()
		#
		# self.logger.info('homed successfully.', extra=self.ext)
		# self.moving = False

	def run_delta_root(self, degrees):
		if self.deg_pos + degrees > self.STOP_LIMIT or self.deg_pos + degrees < -self.STOP_LIMIT:
			return False
