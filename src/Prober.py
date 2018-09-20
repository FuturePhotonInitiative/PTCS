import json
import sys
import pyvisa
import serial.tools.list_ports


def attach_serial(manager, default):
	"""
	Attaches a device with COM format
	:param manager: A pyVISA resource manager
	:param default:
	:return:
	"""
	print("Finding devices...")
	ports = serial.tools.list_ports.comports(False)
	if default:
		for item in ports:
			if str(item.device) == default:
				return manager.open_resource(default)
		print("Default port not found")

	print("*****Connected Devices*****")
	for item in ports:
		print(item)
	print("***************************")
	port = raw_input("Choose serial device to connect to: ")
	return manager.open_resource(port)


def attach_VISA(manager, default):
	"""
	Attaches device in VISA format
	:param manager: A pyVISA resource manager
	:param default: The default address to connect to or None
	:return: A pyVISA device
	"""
	print("Finding devices...")
	instruments = manager.list_resources()
	if default:
		for item in instruments:
			if str(item) == default:
				return manager.open_resource(default)
		print("Default port not found")

	print("*****Connected Devices*****")
	for item in instruments:
		print(item)
	print("***************************")
	instr = raw_input("Choose instrument to connect to: ")
	return manager.open_resource(instr)


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
	device = None
	if config['Requires']['Type'] == "SERIAL":
		device = attach_serial(manager, config['Requires'].get('Default', None))
	elif config['Requires']['Type'] == "VISA":
		device = attach_VISA(manager, config['Requires'].get('Default', None))

	print(device)


if __name__ == '__main__':
	main()
