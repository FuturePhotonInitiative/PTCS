import json
import sys
import pyvisa
import imp


def attach_VISA(manager, name, default):
	"""
	Attaches device in VISA format
	:param manager: A pyVISA resource manager
	:param name: something
	:param default: The default address to connect to or None
	:return: A pyVISA device
	"""
	instruments = manager.list_resources_info()
	if default:
		for item in instruments.values():
			if str(item.resource_name) == default or item.alias is not None and str(item.alias) == default:
				return manager.open_resource(default, write_termination='\n', read_termination='\n')
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
	return manager.open_resource(instr, read_termination='\n')


def main():
	"""
	Loads Experiment JSON file
	:return: None
	"""
	print('Starting Prober...')
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
	print "Finding Devices...."
	for device in config['Requires']['Devices']:
		devices[device['Name']] = attach_VISA(manager, device['Name'], device.get('Default', None))
	for key in devices.keys():
		print key
	# device = attach_VISA(manager, config['Requires'].get('Default', None))
	# Run filepath test
	print "Importing file path..."
	testfile = imp.load_source('voltage_test', config['TestScript']['Filepath'])
	testfile.run(devices)

	# typ = config['Requires']['Devices']['Type']
	# example = imp.load_source(typ, "SPAE\\src\\Instruments\\"+typ+".py")
	# with example.AgilentE3643A(devices[config['Requires']['Devices']['Name']]) as device:
	#  		device.who_am_i()


if __name__ == '__main__':
	main()
