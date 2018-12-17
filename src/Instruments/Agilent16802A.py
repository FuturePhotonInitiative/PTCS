import inspect
import re

import win32com.client
import win32com
import matplotlib.pyplot as plt


class Agilent16802A(object):
	methods = []

	def __init__(self, IP):
		self.IP = IP
		self.connect = win32com.client.Dispatch("AgtLA.Connect")
		self.instance = self.connect.GetInstrument(IP)
		self.module = None
		self.busSignals = None
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		print "Agilent Exiting"

	def who_am_i(self):
		if self.check_connected():
			return "Agilent16802A at " + self.IP
		else:
			return "Agilent16802A DISCONNECTED"

	def check_connected(self):
		return self.instance.IsOnline()[0]

	def what_can_i(self):
		if len(Agilent16802A.methods) == 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					Agilent16802A.methods.append(method)
		return Agilent16802A.methods

	def run_load_config(self, path):
		"""
		This will load a config file given a file path, NOTE: throws exception if config is already loaded
		:param path: The path on the logic analyzer to the config file
		:return: None
		"""
		self.instance.Open(path)

	def run_open_module(self, module):
		"""
		Opens one of the hardware modules on the logic analyzer
		:param module: The name or index of the module to open
		:return: None
		"""
		if isinstance(module, str):
			self.module = self.instance.GetModuleByName(module)
		elif isinstance(module, int):
			self.module = self.instance.Modules(module)

	def run_start_capture(self, async=True, timeout=10):
		"""
		Starts a capture on the logic analyzer, can be told to wait for completion
		:param async: If True this will immediately return after starting the capture, otherwise it will wait for the
			capture to complete
		:param timeout: The maximum time to wait if not asynchronous
		:return: None
		"""
		self.instance.Run()
		if not async:
			self.instance.WaitComplete(timeout)
		self.busSignals = None

	def run_get_bus(self, bus_name):
		"""
		Retrieves a bus from the logic analyzer
		:param bus_name: The name of the bus to retrieve
		:return: The requested Bus or None
		"""
		if self.busSignals is None:
			self.busSignals = self.module.BusSignals
		for index in range(self.busSignals.Count):
			if self.busSignals.Item(index).Name == bus_name:
				return self.busSignals.Item(index)

	def run_get_bus_data(self, bus, output_chars=True):
		"""
		Gets the data associated with a bus from the last sample
		:param bus: The name or instance of the bus to get data from
		:param output_chars: If true the sample is converted to an int
		:return:
		"""
		inner_bus = bus
		if isinstance(bus, str):
			inner_bus = self.run_get_bus(bus)
		bus_data = inner_bus.BusSignalData
		bus_type = inner_bus.BusSignalType
		if bus_data.Type == "Sample":
			sample_data = win32com.client.CastTo(bus_data, "ISampleBusSignalData")
			result = sample_data.GetDataByTime(-float("inf"), float("inf"), bus_type)[0]
			if not output_chars:
				result = [ord(i) for i in result]
			return result

	def run_get_bus_info(self, bus):
		"""
		Gets information associated with a bus from the last sample
		:param bus: The name or instance of the bus to get data from
		:return: A dict containing useful information
		"""
		inner_bus = bus
		if isinstance(bus, str):
			inner_bus = self.run_get_bus(bus)
		bus_data = inner_bus.BusSignalData
		if bus_data.Type == "Sample":
			sample_data = win32com.client.CastTo(bus_data, "ISampleBusSignalData")
			bus_start_time = sample_data.StartTime
			bus_end_time = sample_data.EndTime
			bus_sample_count = (abs(sample_data.StartSample) + abs(sample_data.EndSample))
			return {'Start_Time': bus_start_time, 'End_Time': bus_end_time, 'Sample_Count': bus_sample_count, 'Bits': inner_bus.BitSize, "Bytes": inner_bus.BytesSize}

	@staticmethod
	def dec_range(start, end, step):
		"""
		Port of built in generator "Range" for floating point and decimal numbers
		:param start: The starting decimal
		:param end: The ending decimal
		:param step: The interval of the range
		:return: A list of decimals
		"""
		result = []
		value = start
		while value <= (end + step):
			result.append(value)
			value += step
		return result

	def run_attach_time_to_sample(self, bus, zipped=False, output_chars=True):
		"""
		Attaches each sample to its corresponding time
		:param bus: The name or instance of the bus to get data from
		:param zipped: If true this will Zip the results into a list of tuples, otherwise two lists are returned
		:param output_chars: If true the sample is converted to an int
		:return: Either a list of zipped tuples or a tuple with two lists
		"""
		inner_bus = bus
		if isinstance(bus, str):
			inner_bus = self.run_get_bus(bus)
		bus_info = self.run_get_bus_info(inner_bus)
		sample_rate = (abs(bus_info['Start_Time']) + abs(bus_info['End_Time'])) / (bus_info['Sample_Count'])
		y_axis = self.run_get_bus_data(inner_bus, output_chars)
		x_axis = self.dec_range(bus_info['Start_Time'], bus_info['End_Time'], sample_rate)

		if zipped:
			temp = zip(x_axis, y_axis)
		else:
			temp = (x_axis, y_axis)
		return temp

	def run_display_bus(self, bus):
		"""
		Displays the data from a bus
		:param bus: The name or instance of the bus to get data from
		:return: None
		"""
		inner_bus = bus
		if isinstance(bus, str):
			inner_bus = self.run_get_bus(bus)
		points = self.run_attach_time_to_sample(inner_bus, False)

		plt.plot(points[0], points[1])

		plt.show()
