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
	scripts = {}
	for item in json_file['Experiment']:
		if item['Order'] in scripts.keys():
			scripts[item['Order']].append(item['Source'])
		else:
			scripts[item['Order']] = [item['Source']]
	sorted_scripts = []
	for key in sorted(scripts.keys()):
		sorted_scripts.append(scripts[key])
	return sorted_scripts


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
	manager = pyvisa.ResourceManager()
	devices = {}
	scripts = extract_scripts(config)
	print "Finding Drivers...."
	drivers = os.listdir('./Instruments')
	drivers = [i for i in drivers if not (i == '__init__.py' or i[-3:] != '.py')]

	print "Finding Devices...."
	with contextlib2.ExitStack() as stack:
		for device in config['Requires']['Devices']:
			connection = None
			if device['Type'] is "VISA":
				connection = attach_VISA(manager, device['Name'], device.get('Default', None))
			else:
				connection = raw_input("\'" + device['Name'] + "\' cannot be used with VISA, Please enter connection info (eg. IP address): ")

			driver = device['Driver']
			if driver in drivers:
				if driver not in [i[0] for i in globals().items() if isinstance(i[1], types.ModuleType)]:
					__import__(driver, locals(), globals())
				devices[device['Name']] = stack.enter_context(inspect.getmembers(driver, inspect.isclass)[0][1](connection))

		for frame in scripts:
			threads = []
			for task in frame:
				module = task['Source'][:-3]
				if module not in [i[0] for i in globals().items() if isinstance(i[1], types.ModuleType)]:
					__import__(module, locals(), globals())




if __name__ == '__main__':
	main()
