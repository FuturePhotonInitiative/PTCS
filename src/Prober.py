import inspect
import json
import re
import sys
import types

import pyvisa
import os
import contextlib2
import imp
instruments = None


def attach_VISA(manager, name, default):
	"""
	Attaches device in VISA format, will scan for devices once because it is a slow process, caches results for future
		use. This will attempt to connect to a default address if it is specified in the JSON config, otherwise it will
		prompt the user to input an address from the list of currently connected devices.
	:param manager: A pyVISA resource manager
	:param name: The name of the device being connected
	:param default: The default address to connect to or None
	:return: A pyVISA device
	"""
	global instruments
	if instruments is None:
		instruments = manager.list_resources_info()

	if default:
		for item in instruments.values():
			if str(item.resource_name) == default or item.alias is not None and str(item.alias) == default:
				return manager.open_resource(default)
		print("The default port " + default + " for " + name + " could not be found, please select it manually")
	else:
		print("The default port for " + name + " was not specified, please choose one manually")

	print("*****Connected Devices*****")
	for item in instruments.values():
		line = item.resource_name
		if item.alias is not None:
			line += " -> '" + item.alias + "'"
		print(line)
	print("***************************")
	instr = raw_input("Choose instrument to connect to: ")
	return manager.open_resource(instr)


def extract_scripts(json_file, json_locations):
	"""
	Extracts the scripts from the JSON config and stages them for execution. This will put the scripts in an ordered
		list where each element is a list of tasks to be spawned in parallel
	:param json_file: The JSON config object
	:param json_locations: The JSON Files object with standard file directories
	:return: The list of staged task lists
	"""
	scripts_root = str(json_locations['Files'].get('Script_Root', './Scripts'))
	if scripts_root[0] is '.':
		scripts_root = os.path.join(os.path.dirname(__file__), scripts_root)
	available_scripts = os.listdir(scripts_root)
	available_scripts = [i for i in available_scripts if not (i == '__init__.py' or i[-3:] != '.py')]

	scripts = {}
	for item in [i for i in json_file['Experiment'] if i['Type'] == "PY_SCRIPT"]:

		if str(item['Source']) not in available_scripts:
			sys.exit("Required script \'" + item['Source'] + "\' not found")

		if item['Order'] in scripts.keys():
			scripts[item['Order']].append(item['Source'])
		else:
			scripts[item['Order']] = [item['Source']]
	sorted_scripts = []
	for key in sorted(scripts.keys()):
		sorted_scripts.append(scripts[key])
	return sorted_scripts


def connect_devices(json_file, json_locations, exit_stack):
	"""
	Initializes all devices specified in the JSON config, this will also dynamically import the drivers specified if one
		hasn't been imported already
	:param json_file: Ths JSON config object
	:param json_locations: The JSON Files object with standard file directories
	:param exit_stack: A Exit Stack that will close all devices when the program exits
	:return: A dict of device names mapping to their objects
	"""
	manager = pyvisa.ResourceManager()
	driver_root = str(json_locations['Files'].get('Driver_Root', './Instruments'))
	if driver_root[0] is '.':
		driver_root = os.path.join(os.path.dirname(__file__), driver_root)
	drivers = os.listdir(driver_root)
	drivers = [i[:-3] for i in drivers if not (i == '__init__.py' or i[-3:] != '.py')]
	devices = {}

	print "Finding Devices...."

	# this will need to be edited with using Devices.json as a hardware manager
	with open(json_locations["Files"]["Hardware_Config"]) as d:
		hardware_manager = json.load(d)
	# this one is updated for the hardware manager
	for dev in json_file['Devices']:
		if dev not in hardware_manager.keys():
			print "Device not found in Devices.json: "+dev
		else:
			connection = None
			device = hardware_manager[dev]
			print device
			if str(device['Type']) == "VISA":
				connection = attach_VISA(manager, str(dev), str(device['Default']))
			elif str(device['Type']) == "DIRECT" and "Default" in device.keys():
				connection = str(device['Default'])
			else:
				connection = raw_input(
					"\'" + str(dev) + "\' cannot be used with VISA, Please enter connection info (eg. IP address): ")

			driver = str(device['Driver'])
			if driver in drivers:
				if driver not in [i[0] for i in globals().items() if isinstance(i[1], types.ModuleType)]:
					globals()[driver] = imp.load_source(driver, driver_root + '\\' + driver + '.py')
				devices[str(dev)] = exit_stack.enter_context(inspect.getmembers(globals()[driver],
				                                             inspect.isclass)[0][1](connection))
			else:
				sys.exit("Driver file for \'" + driver + "\' not found in Driver Root: \'" + driver_root)
	return devices


def spawn_scripts(scripts, data_map, json_locations):
	"""
	Runs the scripts defined in the JSON config. The tasks are called based on the order specified in the config,
		two different tasks can have the same order, meaning they should be spawned at the same time.
	:param scripts: The scripts pulled from the config
	:param data_map: The dictionary to store data between tasks
	:param json_locations: The JSON Files object with standard file directories
	:return: None
	"""
	script_root = str(json_locations['Files'].get('Script_Root', './Scripts'))
	if script_root[0] is '.':
		script_root = os.path.join(os.path.dirname(__file__), script_root)

	for frame in scripts:
		threads = []
		for task in frame:  # Add Multi-Threading support here
			module = str(task)[:-3]
			if module not in [i[0] for i in globals().items() if isinstance(i[1], types.ModuleType)]:
				globals()[module] = imp.load_source(module, script_root + '\\' + module + '.py')
			[i[1] for i in inspect.getmembers(globals()[module], inspect.isfunction) if i[0] is 'main'][0](data_map)
	print "Scripts Completed"
	return


def initialize_data(data_map, json_file):
	"""
	Initializes optional Data section of the JSON config into the data map for the tasks
	:param data_map: The dictionary to store data between tasks
	:param json_file: The JSON config object
	:return: None
	"""
	data_section = json_file.get('Data', None)
	if data_section is None:
		return
	data_map['Data']['Initial'] = {}
	for key in data_section.keys():
		data_map['Data']['Initial'][key] = data_section[key]
	return


def check_config_file(config):
	"""
	Checks the config file to ensure that information is properly input in json configuration
	This is specific to the current configuration file and will need to change when the file changes
	:param config, json dictionary containing all information
	:return: problems, array of things wrong with the configuration file
	"""
	problems = []
	with open("../Configs/Files.json") as f:
		files = json.load(f)
	devices = config["Devices"]
	experiments = config["Experiment"]
	with open(files["Hardware_Config"]) as d:
		hardware_manager = json.load(d)
	if "Name" not in config.keys():
		problems.append("Name : does not exist in configuration file")
	for fil in ["Script_Root", "Driver_Root"]:
		if fil not in files.keys():
			problems.append("Files-"+fil+" : does not exist in configuration file")
		else:
			if not os.path.exists(files[fil]):
				problems.append("Files-"+fil+" : path does not exist")
	for device in devices:
		if device not in hardware_manager.keys():
			problems.append("Devices-"+device+" : device not found in hardware manager. Check spelling.")
		else:
			for key in hardware_manager[device].keys():
				if key not in ["Driver", "Type", "Default"]:
					problems.append(device+"-"+key+" : improper structure of json hardware manager file.")
	for experiment in experiments:
		for exp in ["Type", "Source", "Order"]:
			if exp not in experiment.keys():
				problems.append("Experiment-"+exp+" : does not exist in configuration file")
	return problems


def parse_command_line_definitions(data_dict, args):
	"""
	Parses experiment parameters provided at the command line and adds them to the data dictionary.
	:param data_dict:
		The initialized data dictionary
	:param args:
		The argument list, not including the program name (sys.argv[0]) or JSON config file (sys.argv[1]).
		It is recommended to call this using python list slicing (sys.argv[2:]).
	:return:
		None
	"""
	for var in args:
		variable = re.split("=", var)
		# Match numbers and convert them into floats, otherwise leave the input alone
		# (No, we don't yet handle lists or objects, even though they're both valid JSON types)
		if re.match('^[0-9]*\.?[0-9]*$', variable[1]):
			variable[1] = float(variable[1])
		# The config data is stored in two places in the data map
		data_dict['Config']['Data'][variable[0]] = variable[1]
		data_dict['Data']['Initial'][variable[0]] = variable[1]


def main():
	"""
	Entry point of SPAE, loads config file
	:return: None
	"""
	print('Starting SPAE...')
	if len(sys.argv) == 1:
		file_name = raw_input("Enter config file name or nothing to exit: ")
		if len(file_name) == 0:
			print('Goodbye')
			exit(1)
	else:
		file_name = sys.argv[1]

	with open(file_name) as f:
		config = json.load(f)

	with open("../Configs/Files.json") as f:
		files_config = json.load(f)

	# Configuration file check. Ensures the configuration files are formatted properly
	check = check_config_file(config)
	if len(check) is not 0:
		print "ABORTING! Configuration file not formatted correctly."
		for problem in check:
			print problem

	else:
		print("Running Experiment: " + config['Name'] + "\n\n")

		scripts = extract_scripts(config, files_config)

		data_map = {'Data': {}, 'Config': config}

		with contextlib2.ExitStack() as stack:
			data_map['Devices'] = connect_devices(config, files_config, stack)
			initialize_data(data_map, config)
			# There are config definitions in the command line
			# we need to update these here since the data_map is not initialized until near above here
			if len(sys.argv) > 2:
				print "Variable inputs provided."
				parse_command_line_definitions(data_map, sys.argv[2:])
			spawn_scripts(scripts, data_map, files_config)

		print 'Experiment complete, goodbye!'


if __name__ == '__main__':
	main()
