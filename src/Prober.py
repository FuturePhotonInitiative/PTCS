import inspect
import json
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


def extract_scripts(json_file):
	"""
	Extracts the scripts from the JSON config and stages them for execution. This will put the scripts in an ordered
		list where each element is a list of tasks to be spawned in parallel
	:param json_file: The JSON config object
	:return: The list of staged task lists
	"""
	scripts_root = str(json_file['Requires']['Files'].get('Script_Root', './Scripts'))
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


def connect_devices(json_file, exit_stack):
	"""
	Initializes all devices specified in the JSON config, this will also dynamically import the drivers specified if one
		hasn't been imported already
	:param json_file: Ths JSON config object
	:param exit_stack: A Exit Stack that will close all devices when the program exits
	:return: A dict of device names mapping to their objects
	"""
	manager = pyvisa.ResourceManager()
	driver_root = str(json_file['Requires']['Files'].get('Driver_Root', './Instruments'))
	if driver_root[0] is '.':
		driver_root = os.path.join(os.path.dirname(__file__), driver_root)
	drivers = os.listdir(driver_root)
	drivers = [i[:-3] for i in drivers if not (i == '__init__.py' or i[-3:] != '.py')]
	devices = {}

	print "Finding Devices...."

	for device in json_file['Requires']['Devices']:
		connection = None
		if str(device['Type']) == "VISA":
			connection = attach_VISA(manager, str(device['Name']), device.get('Default', None))
		else:
			connection = raw_input(
				"\'" + str(device['Name']) + "\' cannot be used with VISA, Please enter connection info (eg. IP address): ")

		driver = str(device['Driver'])
		if driver in drivers:
			if driver not in [i[0] for i in globals().items() if isinstance(i[1], types.ModuleType)]:
				globals()[driver] = imp.load_source(driver, driver_root + '\\' + driver + '.py')
			devices[str(device['Name'])] = exit_stack.enter_context(inspect.getmembers(globals()[driver], inspect.isclass)[0][1](connection))
		else:
			sys.exit("Driver file for \'" + driver + "\' not found in Driver Root: \'" + driver_root)
	return devices


def spawn_scripts(scripts, data_map, json_file):
	"""
	Runs the scripts defined in the JSON config. The tasks are called based on the order specified in the config,
		two different tasks can have the same order, meaning they should be spawned at the same time.
	:param scripts: The scripts pulled from the config
	:param data_map: The dictionary to store data between tasks
	:param json_file: The JSON config object
	:return: None
	"""
	script_root = str(json_file['Requires']['Files'].get('Script_Root', './Scripts'))
	if script_root[0] is '.':
		script_root = os.path.join(os.path.dirname(__file__), script_root)

	for frame in scripts:
		threads = []
		for task in frame:  # Add Multi-Threading support here
			module = str(task)[:-3]
			if module not in [i[0] for i in globals().items() if isinstance(i[1], types.ModuleType)]:
				globals()[module] = imp.load_source(module, script_root + '\\' + module + '.py')
			[i[1] for i in inspect.getmembers(globals()[module], inspect.isfunction) if i[0] is 'main'][0](data_map)
	print "DONE " + str(data_map['Data'])
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

	print("Running Experiment: " + config['Name'] + "\n\n")

	scripts = extract_scripts(config)

	data_map = {'Data': {}, 'Config': config}

	with contextlib2.ExitStack() as stack:
		data_map['Devices'] = connect_devices(config, stack)
		initialize_data(data_map, config)
		spawn_scripts(scripts, data_map, config)

	print 'Experiment complete, goodbye!'


if __name__ == '__main__':
	main()
