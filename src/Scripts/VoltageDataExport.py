def main(data_map):
	results = data_map['Data']['Reduce']

	for voltage in results.keys():
		print voltage + "\t|\t" + results[voltage]

	return
