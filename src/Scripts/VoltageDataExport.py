import matplotlib.pyplot as plt
import os
import sys
import time


def main(data_map):
	results_reduce = data_map['Data']['Reduce']
	results_collect = data_map['Data']['Collect']
	config = data_map['Config']
	# create unique file with time stamp and name of experiment
	identifier = time.strftime("%m%d%Y_%H%M%S", time.gmtime())+"_"+str(data_map['Config']['Name'].replace(' ', '_'))
	print identifier
	os.chdir("../../")

	if not os.path.exists("Results"):
		os.mkdir("Results")
	os.chdir("Results")

	if not os.path.exists(identifier):
		os.mkdir(identifier)
	os.chdir(identifier)

	# Writing the config file in json format for future use
	with open("config.json", "w+") as config_file:
		config_file.write(str(config).replace('}, ', '}, \n').replace('], ', '], \n').replace("\'", "\""))

	x_axis = []
	y_axis = []
	# Writing out collect results
	with open("collect_results.csv", "w+") as collect_csv:
		collect_csv.write('Voltage,Logic Data\n')
		for voltage in results_collect.keys():
			collect_csv.write(str(voltage))
			for logic in results_collect[voltage]:
				collect_csv.write(','+str(logic))
			collect_csv.write('\n')

	# Writing out and plotting reduce results
	with open("reduce_results.csv", "w+") as reduce_csv:
		reduce_csv.write('Voltage,Percentage\n')
		for voltage in results_reduce.keys():
			print str(voltage)+' : '+str(results_reduce[voltage])
			reduce_csv.write(str(voltage)+','+str(results_reduce[voltage])+'\n')
			x_axis.append(float(voltage))
			y_axis.append(results_reduce[voltage])

	# Plot out Reduced Results
	plt.scatter(x_axis, y_axis)
	plt.autoscale()
	plt.xlabel('Voltage')
	plt.ylabel('Percentage of 1\'s')
	plt.show()

	# save plot in folder somehow? Look into this tomorrow morning
