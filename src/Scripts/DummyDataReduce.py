def main(data_map, experiment_result):
	"""
	This stage calculates the detection percentage for a given applied voltage
	:param data_map: The dictionary to store data between tasks
	:return: None
	"""
	samples = data_map['Data']['Collect']
	# print samples
	data_map['Data']['Reduce'] = {}

	for voltage in list(samples.keys()):
		percent = sum(samples[voltage])/len(samples[voltage])
		data_map['Data']['Reduce'][voltage] = percent
	return
