import time
import re
import inspect
import numpy
import pyvisa


class AQ6317(object):
	"""
	This class models the AndoAQ6317 optical spectrum Analyzer.

	.. note::
	Currently this class and therefore get_o_spectrum()
	is explicitly written to set up the connection and
	work only with the AQ4321 Laser.
	"""

	methods = []

	def __init__(self, device):
		"""
		Constructor method.
		standard address='GPIB0::2::INSTR'
		:param device: device from PyVisa open_resource object
		:type: PyVisa open_resource object
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
		"""
		:returns: reference to device
		"""
		if self.check_connected():
			return "Ando AQ6317 at " + self.device.resource_info[0].alias
		else:
			return "Ando AQ6317 DISCONNECTED"

	def what_can_i(self):
		"""
		:returns: instrument attributes
		"""
		if len(AQ6317.methods) is 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					AQ6317.methods.append(method)
		return AQ6317.methods

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def run_get_o_spectrum(self, start, stop, step):

		self.device.write('SNHD')  # Sets Sensitivity to Normal Range (HOLD)
		self.device.write('AVG1')  # Sets the number of averaging times for measurement to 1
		self.device.write('TLSADR24')  # Sets the GPIB Address of Laser to 24
		self.device.write('TLSADR?')  # Double checks that it is set
		info = self.device.read()
		print ('Laser Address Set At: ' + info)

		self.device.write('GP2ADR20')  # Sets the GPIB of OSA to 20
		self.device.write('GP2ADR?')  # Double checks
		info = self.device.read()
		print ('GP-IB2 Address of OSA set to: ' + info)

		self.device.write('TLSSYNC1')  # Syncs Laser and OSA
		self.device.write('TLSSYNC?')  # Double checks
		info = self.device.read()
		print ('Laser and OSA Link Status: ' + info)
		# 1 on, 0 off

		start = float(start)
		stop = float(stop)
		step = float(step)
		self.device.write('RESLN2')  # set to lowest resolution, step size now indicates resolution
		self.device.write('SRMSK254')  # Sets mask to be 254, Masking for 'Sweep Complete' (Bit 0)
		self.device.write('SRQ1')  # Status Bit on

		# Not sure if this will work or not. Take a closer look into read_stb() and figure out
		# how it's invoked for what was gpib and how resource uses it
		self.device.read_stb()     # Discard Initial status bit

		sweep_width = stop - start
		sample_number = sweep_width / step + 1

		self.device.write('SMPL' + str(sample_number))  # Resolution of sweep
		self.device.write('STAWL' + str(start))  # Beginning of sweep
		self.device.write('STPWL' + str(stop))  # End of sweep

		print('Scan Starts: ' + str(start) + ' to ' + str(stop) + ' at ' + str(step) + 'nm step')

		self.device.write('SGL')  # Start Single Sweep

		self.run_check_status()  # Checks if sweep is complete

		print('[Sweep Done]')
		# time.sleep(60)

		self.device.write('SD1, LDATA')  # Reads Data from Buffer
		self.device.read()
		data_list = []

		for x in numpy.arange(float(start), float(stop) + float(step), float(step)):
			reading = float(self.device.read().strip(' \t\r\n'))  # Strips all blank space characters. Readings in dBm
			if -200 < reading < 100:  # If readings within reasonable range, append
				data_list.append([x, reading])

		return data_list

	def run_check_status(self):
		status = int(self.device.read_stb())
		print('Status: %d' % status)
		print('Scanning.'),
		while status == 0:
			time.sleep(0.5)
			status = int(self.device.read_stb())
			print('.'),
		return True
