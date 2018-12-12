def main(data_map):
	samples = data_map['Data']['Collect']
	data_map['Data']['Reduce'] = {}

	for voltage in samples.keys():
		percent = sum(samples[voltage])/len(samples[voltage])
		data_map['Data']['Reduce'][voltage] = percent

	return
