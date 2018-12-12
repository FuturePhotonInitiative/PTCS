def main(data_map):
	results = data_map['Data']['Reduce']

	for voltage in results.keys():
		print str(voltage) + "\t|\t" + str(results[voltage])

	return
