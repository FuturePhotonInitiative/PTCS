import inspect
import re
import pyvisa


class VCU108(object):
	methods = []

	def __init__(self, device):
		self.device = device
		self._locked = False
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.device.close()
		pass

	def who_am_i(self):
		if self.check_connected():
			return "VCU108 at " + self.device.resource_info[0].alias
		else:
			return "VCU108 DISCONNECTED"

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def what_can_i(self):
		if len(VCU108.methods) == 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					VCU108.methods.append(method)
		return VCU108.methods

	def run_eye_scan(self, scale_factor=0, horizontal_boundary=4, vertical_boundary=1, points=0, drp=0):
		data = []
		if not self.check_connected():
			return False
		else:
			self.device.write("G")
			self.device.write(str(scale_factor))
			self.device.write(str(horizontal_boundary))
			self.device.write(str(vertical_boundary))
			self.device.write(str(points))
			self.device.write(str(drp))
			line = ""
			while "END" not in line:
				try:
					line = self.device.read()
					print line
					data.append(line)
				except pyvisa.errors.VisaIOError:
					continue
			return data

	def run_raw_command(self, command):
		if not self.check_connected():
			return False
		else:
			return self.device.query(command)

	def run_petb_read(self, pin):
		"""
		petb gpio read [port=0] [pin], port is always 0
		:param pin: string, pin value, must be in valid_pins
		:return: data, all data from command, will need to be parsed later
		"""
		valid_pins = ["modsel", "reset", "modprs", "int", "lpmode", "all"]
		if not self.check_connected():
			return False
		else:
			if pin not in valid_pins:
				return "Invalid pin sent."
			return self.device.query("petb gpio read 0 "+str(pin))

	def run_petb_set(self, pin):
		"""
		petb gpio write [port=0] [pin], port is always 0
		:param pin: string, pin value, must be in valid_pins
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_pins = ["modsel", "reset", "modprs", "int", "lpmode", "all"]
		if not self.check_connected():
			return False
		else:
			if pin not in valid_pins:
				return "Invalid pin sent."
			return self.device.query("petb gpio set 0 "+str(pin))

	def run_petb_clear(self, pin):
		"""
		petb gpio write [port=0] [pin], port is always 0
		:param pin: string, pin value, must be in valid_pins
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_pins = ["modsel", "reset", "modprs", "int", "lpmode", "all"]
		if not self.check_connected():
			return False
		else:
			if pin not in valid_pins:
				return "Invalid pin sent."
			return self.device.query("petb gpio clear 0 "+str(pin))

	def run_petb_toggle(self, pin):
		"""
		petb gpio write [port=0] [pin], port is always 0
		:param pin: string, pin value, must be in valid_pins
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_pins = ["modsel", "reset", "modprs", "int", "lpmode", "all"]
		if not self.check_connected():
			return False
		else:
			if pin not in valid_pins:
				return "Invalid pin sent."
			return self.device.query("petb gpio toggle 0 "+str(pin))

	def run_pek_read(self, pin=0, port=0):
		"""
		pek gpio read [port=0] [pin=0]
		:param pin: string, pin value, must be in valid_pins
		:param port: int, port number, must be in valid_ports
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_pins = [0, 1, 2, 3, 4, 5, 6, 7]
		valid_ports = [0, 1, 2, 3]

		if not self.check_connected():
			return False
		else:
			if pin not in valid_pins:
				print "Invalid pin sent."
				return False
			if port not in valid_ports:
				print "Invalid port sent."
				return False
			return self.device.query("pek gpio read " + str(port) + " " + str(pin))

	def run_pek_set(self, pin=0, port=0):
		"""
		pek gpio set [port=0] [pin=0]
		:param pin: string, pin value, must be in valid_pins
		:param port: int, port number, must be in valid_ports
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_pins = [0, 1, 2, 3, 4, 5, 6, 7]
		valid_ports = [0, 1, 2, 3]

		if not self.check_connected():
			return False
		else:
			if pin not in valid_pins:
				print "Invalid pin sent."
				return False
			if port not in valid_ports:
				print "Invalid port sent."
				return False
			return self.device.query("pek gpio set " + str(port) + " " + str(pin))

	def run_pek_clear(self, pin=0, port=0):
		"""
		pek gpio clear [port=0] [pin=0]
		:param pin: string, pin value, must be in valid_pins
		:param port: int, port number, must be in valid_ports
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_pins = [0, 1, 2, 3, 4, 5, 6, 7]
		valid_ports = [0, 1, 2, 3]

		if not self.check_connected():
			return False
		else:
			if pin not in valid_pins:
				print "Invalid pin sent."
				return False
			if port not in valid_ports:
				print "Invalid port sent."
				return False
			return self.device.query("pek gpio clear " + str(port) + " " + str(pin))

	def run_pek_toggle(self, pin=0, port=0):
		"""
		pek gpio toggle [port=0] [pin=0]
		:param pin: string, pin value, must be in valid_pins
		:param port: int, port number, must be in valid_ports
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_pins = [0, 1, 2, 3, 4, 5, 6, 7]
		valid_ports = [0, 1, 2, 3]

		if not self.check_connected():
			return False
		else:
			if pin not in valid_pins:
				print "Invalid pin sent."
				return False
			if port not in valid_ports:
				print "Invalid port sent."
				return False
			return self.device.query("pek gpio toggle " + str(port) + " " + str(pin))

	def run_pek_write(self, pin=0, port=0, value=0):
		"""
		pek gpio write [port=0] [pin=0]
		:param pin: string, pin value, must be in valid_pins
		:param port: int, port number, must be in valid_ports
		:param value: int, value, must be 0 or 1
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_pins = [0, 1, 2, 3, 4, 5, 6, 7]
		valid_ports = [0, 1, 2, 3]
		valid_values = [0, 1]

		if not self.check_connected():
			return False
		else:
			if pin not in valid_pins:
				print "Invalid pin sent."
				return False
			if port not in valid_ports:
				print "Invalid port sent."
				return False
			if value not in valid_values:
				print "Invalid port sent."
				return False
			return self.device.query("pek gpio write " + str(port) + " " + str(pin) + " " + str(value))

	def run_pek_list(self):
		"""
		pek gpio list
		:return: data, all data from command, will need to be parsed later
		"""
		data = []

		if not self.check_connected():
			return False
		else:
			return self.device.query("pek gpio list")

	def run_adc_read(self, channel="00"):
		"""
		adc read [channel]
		:param channel: string, must be in valid_channels
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_channels = ["00", "0e", "10", "13", "16", "17"]

		if not self.check_connected():
			return False
		else:
			if channel not in valid_channels:
				print "Channel not valid."
				return False
			return self.device.query("adc read " + str(channel))

	def run_dac_write(self, value=""):
		"""
		dac write []
		:param value: string, data to be written to the DAC
		:return: data, all data from command, will need to be parsed later
		"""
		data = []

		if not self.check_connected():
			return False
		else:
			return self.device.query("dac write " + str(value))

	def run_spixfer(self, value):
		"""
		spixfer [string]
		:param value: string, data to be written to SPI
		:return: data, all data from command, will need to be parsed later
		"""
		data = []

		if not self.check_connected():
			return False
		else:
			return self.device.query("spixfer " + str(value))

	def run_spilib(self, value):
		"""
		spilib [string]
		:param value: string, data to be written to SPI
		:return: data, all data from command, will need to be parsed later
		"""
		data = []

		if not self.check_connected():
			return False
		else:
			return self.device.query("spilib "+str(value))

	def run_i2cwrite(self, address, value):
		"""
		i2cwrite [address] [byte value]
		:param address: string, must be between 0x00 and 0xFF
		:param value: string, byte value to write to address
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_address = re.compile(r'(?P<name>0x[0-9ABCDEF][0-9ABCDEF])')
		match = valid_address.match(address)

		if not self.check_connected():
			return False
		else:
			if match is None:
				print "Enter a valid address"
				return False
			return self.device.query("i2cwrite " + str(address) + " " + str(value))

	def run_i2cread(self, address, value=""):
		"""
		i2cwrite [address] [byte value]
		:param address: string, must be between 0x00 and 0xFF
		:param value: string, optional, number of bytes to read
		:return: data, all data from command, will need to be parsed later
		"""
		data = []
		valid_address = re.compile(r'(?P<name>0x[0-9ABCDEF][0-9ABCDEF])')
		match = valid_address.match(address)

		if not self.check_connected():
			return False
		else:
			if match is None:
				print "Enter a valid address"
				return False
			return self.device.query("i2cread " + str(address) + " " + str(value))
