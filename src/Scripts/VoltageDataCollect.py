import time


def main(data_map):

	logic_analyzer = data_map['Devices']['Logic_Analyzer']
	# voltage_source = data_map['Devices']['Voltage_Source']
	data_map['Data']['Collect'] = {}
	levels = dec_range(0, 5, 0.05)

	# voltage_source.run_set_voltage(0)
	# voltage_source.set_output_switch(1)

	logic_analyzer.run_open_module(0)

	start_time = time.time()
	for i in levels:
		# voltage_source.run_set_voltage(i)
		time.sleep(0.25)
		logic_analyzer.run_start_capture(False)

		data_map['Data']['Collect'][str(i)] = logic_analyzer.run_attach_time_to_sample('My Bus 1', False)

	print "Collection took: " + str(time.time() - start_time) + " seconds"
	return


def dec_range(start, end, step):
	result = []
	value = start
	while value <= (end + step):
		result.append(value)
		value += step
	return result
