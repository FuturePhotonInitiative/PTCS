import sys
import json
import os
# This file can be deleted as it was created to simply test the function
# The function is currently in Prober.py under check_config_file


def check_config_file(config):
	"""
	Checks the config file to ensure that information is properly input in json configuration
	:param config, json dictionary containing all information
	:return: problems, array of things wrong with the configuration file
	"""
	problems = []
	files = config["Requires"]["Files"]
	devices = config["Requires"]["Devices"]
	experiments = config["Experiment"]
	if "Name" not in config.keys():
		problems.append("Name : does not exist in configuration file")
	for fil in ["Script_Root", "Driver_Root"]:
		if fil not in files.keys():
			problems.append("Requires-Files-"+fil+" : does not exist in configuration file")
		else:
			if not os.path.exists(files[fil]):
				problems.append("Requires-Files-"+fil+" : path does not exist")
	for device in devices:  # this will change when the hardware manager is implemented
							# at that point, only the name of the device will need to be verified
							# as driver and type will already be constants in Devices.json
		for dev in ["Name", "Driver", "Type"]:
			if dev not in device.keys():
				problems.append("Requires-Devices-"+dev+" : does not exist in configuration file")
	for experiment in experiments:
		for exp in ["Type", "Source", "Order"]:
			if exp not in experiment.keys():
				problems.append("Experiment-"+exp+" : does not exist in configuration file")
	return problems


with open(sys.argv[1]) as f:
	configuration = json.load(f)
print check_config_file(configuration)
