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
		self.instance.Open(path)

	def run_open_module(self, module):
		if isinstance(module, str):
			self.module = self.instance.GetModuleByName(module)
		elif isinstance(module, int):
			self.module = self.instance.Modules(module)

	def run_start_capture(self, async=True):
		self.instance.Run()
		if not async:
			self.instance.WaitComplete(10)
		self.busSignals = None

	def run_get_bus(self, bus_name):
		if self.busSignals is None:
			self.busSignals = self.module.BusSignals
		for index in range(self.busSignals.Count):
			if self.busSignals.Item(index).Name == bus_name:
				return self.busSignals.Item(index)

	def run_get_bus_data(self, bus, output_chars=True):
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
		inner_bus = bus
		if isinstance(bus, str):
			inner_bus = self.run_get_bus(bus)
		bus_data = inner_bus.BusSignalData
		if bus_data.Type == "Sample":
			sample_data = win32com.client.CastTo(bus_data, "ISampleBusSignalData")
			bus_start_time = sample_data.StartTime
			bus_end_time = sample_data.EndTime
			bus_sample_count = (abs(sample_data.StartSample) + abs(sample_data.EndSample))
			return {'Start_Time': bus_start_time, 'End_Time': bus_end_time, 'Sample_Count': bus_sample_count}

	@staticmethod
	def dec_range(start, end, step):
		result = []
		value = start
		while value <= (end + step):
			result.append(value)
			value += step
		return result

	def run_attach_time_to_sample(self, bus, zipped=False, output_chars=True):
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
		inner_bus = bus
		if isinstance(bus, str):
			inner_bus = self.run_get_bus(bus)
		points = self.run_attach_time_to_sample(inner_bus, False)

		plt.plot(points[0], points[1])

		plt.show()
