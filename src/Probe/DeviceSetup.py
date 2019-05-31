import pyvisa
import os
import json
import sys
import inspect
import imp
import types


class DeviceSetup:

    # caches results for future queue jobs.
    manager = pyvisa.ResourceManager()
    instruments = manager.list_resources_info()

    def __init__(self):
        pass

    @staticmethod
    def attach_VISA(name, default):
        """
        Attaches device in VISA format, This will attempt to connect to a default address if it is specified in the JSON
        config, otherwise it will prompt the user to input an address from the list of currently connected devices.
        :param name: The name of the device being connected
        :param default: The default address to connect to or None
        :return: A pyVISA device
        """
        if default:
            for item in DeviceSetup.instruments.values():
                if str(item.resource_name) == default or item.alias is not None and str(item.alias) == default:
                    return DeviceSetup.manager.open_resource(default)
            print("The default port " + default + " for " + name + " could not be found, please select it manually")
        else:
            print("The default port for " + name + " was not specified, please choose one manually")

        print("*****Connected Devices*****")
        for item in DeviceSetup.instruments.values():
            line = item.resource_name
            if item.alias is not None:
                line += " -> '" + item.alias + "'"
            print(line)
        print("***************************")
        instr = raw_input("Choose instrument to connect to: ")
        return DeviceSetup.manager.open_resource(instr)

    def connect_devices(self, config_file_devices, file_locations, exit_stack):
        """
        Initializes all devices specified in the JSON config, this will also dynamically import the drivers
        specified if one hasn't been imported already
        :param config_file_devices: The list of devices to be used
        :param file_locations: The JSON Files object with standard file directories
        :param exit_stack: A Exit Stack that will close all devices when the program exits
        :return: A dict of device names mapping to their objects
        """
        driver_root = str(file_locations['Driver_Root'])
        drivers = os.listdir(driver_root)
        drivers = [i[:-3] for i in drivers if not (i == '__init__.py' or i[-3:] != '.py')]
        devices = {}

        print "Finding Devices...."

        with open(file_locations["Hardware_Config"]) as d:
            hardware_manager = json.load(d)
        # this one is updated for the hardware manager
        for dev in config_file_devices:
            if dev not in hardware_manager.keys():
                print "Device not found in Devices.json: " + dev
            else:
                connection = None
                device = hardware_manager[dev]
                print device
                if str(device['Type']) == "VISA":
                    connection = self.attach_VISA(str(dev), str(device['Default']))
                elif str(device['Type']) == "DIRECT" and "Default" in device.keys():
                    connection = str(device['Default'])
                else:
                    connection = raw_input(
                        "\'" + str(
                            dev) + "\' cannot be used with VISA, Please enter connection info (eg. IP address): ")

                driver = str(device['Driver'])
                if driver in drivers:
                    if driver not in [i[0] for i in globals().items() if isinstance(i[1], types.ModuleType)]:
                        globals()[driver] = imp.load_source(driver, driver_root + '\\' + driver + '.py')
                    devices[str(dev)] = exit_stack.enter_context(inspect.getmembers(globals()[driver],
                                                                                    inspect.isclass)[0][1](connection))
                else:
                    sys.exit("Driver file for \'" + driver + "\' not found in Driver Root: \'" + driver_root)
        return devices
