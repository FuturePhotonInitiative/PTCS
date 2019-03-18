import json
import os

from src.GUI.Util.Globals import Hardware


class HardwareManager:
    def __init__(self, hardware_config, driver_root):
        """
        Initializes the hardware manager with a list of drivers and configured hardware devices
        :param hardware_config:
            The .json file which holds the hardware configuration
        :param driver_root:
            The directory which holds all of the hardware drivers
        """
        self.hardware_config = hardware_config
        self.hardware_objects = {}
        self.drivers = []
        with open(hardware_config) as config_file:
            self.hardware_dict = json.load(config_file)
            for hardware_item in self.hardware_dict.keys():
                obj = Hardware(hardware_item,
                               self.hardware_dict[hardware_item]['Driver'],
                               self.hardware_dict[hardware_item]['Type'],
                               self.hardware_dict[hardware_item]['Default'])
                self.hardware_objects[hardware_item] = obj
        self.drivers = os.listdir(driver_root)

    def get_hardware_object(self, name):
        """
        :param name:
            The name of the hardware in the configuration file
        :return:
            A Hardware object representing the configuration of the hardware with the given name
        """
        return self.hardware_objects[name]

    def get_all_hardware_names(self):
        """
        :return:
            A list of all of the names of hardware devices in the configuration file provided on initialization
        """
        return self.hardware_objects.keys()

    def get_drivers(self):
        """
        :return:
            A list of all of the drivers in the Driver_Root directory provided at initialization
        """
        return self.drivers

    def update_hardware_config(self, hardware_object, name=None, commit_changes=False):
        """
        Update the internal representation of the hardware configuration file
        :param hardware_object:
            The hardware object holding the updated values
        :param name:
            If provided, replace the hardware configuration with `name` with the configuration found in hardware_object
        :param commit_changes:
            If true, write the update to disk
        :return:
            None
        """
        if name is not None:
            self.hardware_dict.pop(name)
        self.hardware_dict[hardware_object.name] = {}
        self.hardware_dict[hardware_object.name]['Driver'] = hardware_object.driver
        self.hardware_dict[hardware_object.name]['Type'] = hardware_object.connection_type
        self.hardware_dict[hardware_object.name]['Default'] = hardware_object.default_connection
        if commit_changes:
            self.commit_hardware_config_to_file()

    def commit_hardware_config_to_file(self):
        """
        Write the current state of the hardware configuration to disk with the file name provided as hardware_config
        at initialization
        :return:
            None
        """
        with open(self.hardware_config, "w") as config_file:
            json.dump(self.hardware_dict, config_file)

