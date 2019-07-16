import pyvisa
import os
import json
import sys
import inspect
import imp
import types

from src.GUI.Util import CONSTANTS


class DeviceSetup:

    def __init__(self):
        self.visa_rm = pyvisa.ResourceManager()
        self.available_instruments = self.visa_rm.list_resources_info().values()

    def attach_VISA(self, name, default):
        """
        Attaches device in VISA format, This will attempt to connect to a default address if it is specified in the JSON
        config, otherwise it will prompt the user to input an address from the list of currently connected devices.
        :param name: The name of the device being connected
        :param default: The default address to connect to or None
        :return: A pyVISA device
        """
        if default:
            if default in [i.resource_name for i in self.available_instruments] + \
                          [i.alias for i in self.available_instruments if i.alias is not None] or \
                    default[-6:] == "SOCKET":
                return self.visa_rm.open_resource(default)
            print "'Default' connection string: " + default + " for " + name + " is invalid.",
        else:
            print "The default port for " + name + " was not specified.",
        print(" Do you mean one of these?:")

        print("*****Connected Devices*****")
        for item in self.available_instruments:
            line = item.resource_name
            if item.alias is not None:
                line += " -> '" + item.alias + "'"
            print(line)
        print("***************************")
        instr = raw_input("Choose instrument to connect to: ")
        return self.visa_rm.open_resource(instr)

    def connect_devices(self, config_file_devices, exit_stack):
        """
        Initializes all devices specified in the device list. this will also dynamically import the drivers
        specified if one hasn't been imported already
        :param config_file_devices: The list of devices to be used
        :param exit_stack: A Exit Stack that will close all devices when the program exits
        :return: A dict of device names mapping to their objects
        """
        drivers = os.listdir(CONSTANTS.DRIVERS_DIR)
        drivers = [i[:-3] for i in drivers if not (i == '__init__.py' or i[-3:] != '.py')]
        connected_devices = {}

        print "Finding Devices...."

        with open(CONSTANTS.DEVICES_CONFIG) as d:
            hardware_manager = json.load(d)
        for device_key in config_file_devices:
            if device_key not in hardware_manager.keys():
                print "Device not found in Devices.json: " + device_key
            else:
                connection = None
                device_config = hardware_manager[device_key]
                if str(device_config['Type']) == "VISA":
                    connection = self.attach_VISA(str(device_key), str(device_config['Default']))
                elif str(device_config['Type']) == "DIRECT" and "Default" in device_config.keys():
                    connection = str(device_config['Default'])
                else:
                    connection = raw_input("\'" + str(device_key) + "\' cannot be used with VISA, "
                                                                    "Please enter connection info (eg. IP address): ")

                driver_file_name = str(device_config['Driver'])

                # instantiate a class based on the name of the file it is in.
                if driver_file_name in drivers:
                    if driver_file_name not in [i[0] for i in globals().items() if isinstance(i[1], types.ModuleType)]:
                        globals()[driver_file_name] = imp.load_source(
                                driver_file_name, os.path.join(CONSTANTS.DRIVERS_DIR, driver_file_name + '.py'))
                    DriverClass = [i for i in inspect.getmembers(globals()[driver_file_name], inspect.isclass)
                                   if i[0] == driver_file_name][0][1]
                    connected_devices[device_key] = exit_stack.enter_context(DriverClass(connection))
                else:
                    print("ting")
                    print("Error: Driver file '{}' for '{}' not found in the Driver Root directory '{}'".format(
                            driver_file_name, device_key, CONSTANTS.DRIVERS_DIR))
                    sys.exit(1)
        return connected_devices
