

def main(data_map, experiment_result):
	"""
	This stage saves results into 2 separate CSV files for both collect and reduce
	Also displays and saves a plot of the reduce data
	:param data_map: The dictionary to store data between tasks
	:return: None
	"""
	results_reduce = data_map['Data']['Reduce']
	results_collect = data_map['Data']['Collect']

	# arrays for plotting x and y axis
	x_axis = []
	y_axis = []
	# Writing out collect results to csv
	experiment_result.add_csv_dict("collect_results", results_collect, sorted(results_collect.keys()), column_labels=['Logic Data'], title="Fake Voltage")

	experiment_result.add_csv_dict("reduced_results", results_reduce, sorted(results_reduce.keys()), column_labels=['Logic Data'], title="Fake Voltage")

	# Writing out and plotting reduce results to csv
	for voltage in sorted(results_reduce.keys()):
		x_axis.append(float(voltage))
		y_axis.append(results_reduce[voltage])

	# Plot out Reduced Results
	experiment_result.add_scatter_chart("Fake_Voltage_vs_Current", x_axis, y_axis, x_label="Fake Voltage", y_label = "Fake Current", title="Fake Voltage vs Current")
	# plt.show()

