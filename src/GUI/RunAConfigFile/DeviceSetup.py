import pyvisa
import os
import inspect
import imp
import types
from src.GUI.Util import CONSTANTS

from src.GUI.Application.HardwareManager import HardwareManager


class DeviceSetup:

    def __init__(self):
        self.visa_rm = pyvisa.ResourceManager()
        self.available_instruments = list(self.visa_rm.list_resources_info().values())

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
            print("'Default' connection string: " + default + " for " + name + " is invalid.", end=' ')
        else:
            print("The default port for " + name + " was not specified.", end=' ')
        print(" Do you mean one of these?:")

        print("*****Connected Devices*****")
        for item in self.available_instruments:
            line = item.resource_name
            if item.alias is not None:
                line += " -> '" + item.alias + "'"
            print(line)
        print("***************************")
        instr = input("Choose instrument to connect to: ")
        return self.visa_rm.open_resource(instr)

    def connect_devices(self, config_file_devices, exit_stack):
        """
        Creates connections with all the instruments specified in the incoming devices object. If a driver to an
        instrument was not already imported, it will dynamically import the driver. It also does a final check to query
        the device and verify it returns a value. This means it is actually connected.
        specified if one hasn't been imported already
        :param config_file_devices: The list of devices to be used
        :param exit_stack: A Exit Stack that will close all devices when the program exits
        :return: A dict of device names mapping to their objects
        """
        print("Connecting devices...")
        errors = False
        drivers = os.listdir(CONSTANTS.DRIVERS_DIR)
        drivers = [i[:-3] for i in drivers if not (i == '__init__.py' or i[-3:] != '.py')]
        connected_devices = {}

        hardware_manager = HardwareManager(CONSTANTS.DEVICES_CONFIG)
        for device_key in config_file_devices:
            if device_key not in hardware_manager.get_all_hardware_names():
                print("    Device not found in Devices.json: " + device_key)
            else:
                print("    Connecting to " + device_key + "...", end="")
                connection = None
                device_config = hardware_manager.get_hardware_object(device_key)
                if device_config.uses_pyvisa():
                    try:
                        connection = self.attach_VISA(device_key, device_config.default)
                    except Exception:
                        errors = True
                        print("\n         " + device_key +
                              " did not reciprocate connection. Is the device on and/or physically connected?")
                        continue
                else:
                    connection = device_config.default

                driver_file_name = device_config.driver

                # instantiate a class based on the name of the file it is in.
                if driver_file_name in drivers:
                    if driver_file_name not in [i[0] for i in list(globals().items()) if isinstance(i[1], types.ModuleType)]:
                        globals()[driver_file_name] = imp.load_source(
                                driver_file_name, os.path.join(CONSTANTS.DRIVERS_DIR, driver_file_name + '.py'))

                    DriverClass = [i for i in inspect.getmembers(globals()[driver_file_name], inspect.isclass)
                                   if i[0] == driver_file_name][0][1]

                    driver_object = DriverClass(connection)

                    # check_connected should query the device and verify it gets a response back
                    if not driver_object.check_connected():
                        errors = True
                        print("\n         " + device_key +
                              " did not reciprocate connection. Is the device on and/or physically connected?")
                        continue

                    connected_devices[device_key] = exit_stack.enter_context(driver_object)
                else:
                    errors = True
                    print("\n        Driver file '{}' for '{}' not found in the Driver Root directory '{}'".format(
                            driver_file_name, device_key, CONSTANTS.DRIVERS_DIR))
                    continue
            print("done.")
        if errors:
            return None
        else:
            return connected_devices
