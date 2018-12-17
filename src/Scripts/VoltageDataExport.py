import matplotlib.pyplot as plt
import os
import sys
import time

data = {}
data['Config'] = {
  "Name": "Determine Voltage Threshold",
  "Requires": {
              "Files": {
                        "Script_Root": "./Scripts",
                        "Driver_Root": "./Instruments"
                       },
              "Devices": [
                         {
                           "Name":     "Voltage_Source",
                           "Driver":   "AgilentE3643A",
                           "Type":     "VISA"
                         },
	                     {
		                     "Name": "Logic_Analyzer",
		                     "Driver": "Agilent16802A",
		                     "Type": "Direct"
	                     }
                         ]
              },
  "Experiment": [
                {
                  "Type": "PY_SCRIPT",
                  "Source": "VoltageDataCollect.py",
                  "Order":  1
                },
                {
                  "Type": "PY_SCRIPT",
                  "Source": "VoltageDataReduce.py",
                  "Order":  2
                },
                {
                  "Type": "PY_SCRIPT",
                  "Source": "VoltageDataExport.py",
                  "Order":  3
                }
                ]
}
data["Data"] = {
	  "Collect": {
		  '0.9': [1, 1, 1, 1, 1, 1, 1],
		  '0.8': [1, 1, 1, 1, 1, 1, 1],
		  '0.7': [1, 1, 1, 1, 1, 1, 1],
		  '0.6': [1, 0, 1, 0, 1, 1, 1],
		  '0.5': [0, 0, 1, 1, 0, 0, 0],
		  '0.4': [0, 1, 0, 0, 0, 0, 0],
		  '0.3': [0, 0, 0, 0, 0, 0, 0],
		  '0.2': [0, 0, 0, 0, 0, 0, 0],
		  '0.1': [0, 0, 0, 0, 0, 0, 0],
		  '0.0': [0, 0, 0, 0, 0, 0, 0]
	  },
	  "Reduce": {
		  '0.9': 1.00,
		  '0.8': 1.00,
		  '0.7': 1.00,
		  '0.6': 0.7142,
		  '0.5': 0.2857,
		  '0.4': 0.1429,
		  '0.3': 0.00,
		  '0.2': 0.00,
		  '0.1': 0.00,
		  '0.0': 0.00
	  }
}


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

	sys.exit("Done")


main(data)
