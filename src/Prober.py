import inspect
import json
import sys
import types

import pyvisa
import os
import contextlib2
import importlib
import imp
instruments = None


def attach_VISA(manager, name, default):
	"""
	Attaches device in VISA format
	:param manager: A pyVISA resource manager
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
				# importlib.import_module(driver, driver_root)
				# __import__(driver, locals(), globals())
			devices[str(device['Name'])] = exit_stack.enter_context(inspect.getmembers(globals()[driver], inspect.isclass)[0][1](connection))
		else:
			sys.exit("Driver file for \'" + driver + "\' not found in Driver Root: \'" + driver_root)
	return devices


def spawn_scripts(scripts, data_map, json_file):
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


def main():
	"""
	Loads Experiment JSON file
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
		spawn_scripts(scripts, data_map, config)

	print 'Experiment complete, goodbye!'


if __name__ == '__main__':
	main()
