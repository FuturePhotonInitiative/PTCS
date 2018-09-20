

class VCU108(object):

	def __init__(self, device):
		self.device = device

	def who_am_i(self):
		if self.check_connected():
			return "VCU108 at " + self.device._resource_name
		else:
			return "VCU108 DISCONNECTED"

	def check_connected(self):
		if not self.device:
			return False

		try:
			self.device.session
			return True
		except:
			self.device = None
			return False

	@staticmethod
	def what_can_i():
		return []

	def raw_command(self, command):
		if not self.check_connected():
			return False
