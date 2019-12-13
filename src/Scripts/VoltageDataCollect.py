import time


def main(data_map, experiment_result):
	"""
	This stage varies an applied voltage to a logic analyzer and collects the resulting samples
	:param data_map: The dictionary to store data between tasks
	:return: None
	"""
	logic_analyzer = data_map['Devices']['Logic_Analyzer']
	voltage_source = data_map['Devices']['Voltage_Source']
	data_map['Data']['Collect'] = {}
	start_voltage = float(data_map['Data']['Initial']["Start_Voltage"])
	final_voltage = float(data_map['Data']['Initial']["Final_Voltage"])
	step_voltage = float(data_map['Data']['Initial']["Step_Voltage"])
	levels = dec_range(start_voltage, final_voltage, step_voltage)

	voltage_source.set_voltage(0)
	voltage_source.set_output_switch(1)

	logic_analyzer.open_module(0)

	start_time = time.time()
	for i in levels:
		voltage_source.set_voltage(i)
		# time.sleep(0.25)
		if i % 1 == 0:
			print("Applying " + str(i) + " volts")
		logic_analyzer.start_capture(False)

		data_map['Data']['Collect'][str(i)] = logic_analyzer.get_bus_data('My Bus 1', False)

	voltage_source.set_voltage(0)
	voltage_source.set_output_switch(0)

	print("Collection took: " + str(time.time() - start_time) + " seconds")
	# sys.exit("Done")
	return


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
	if step > 0:
		while value <= (end + step):
			result.append(value)
			value += step
	else:
		while value >= (end + step):
			result.append(value)
			value += step
	return result
