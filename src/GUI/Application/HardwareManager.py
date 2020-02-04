import json

from src.GUI.Model.HardwareModel import HardwareModel

from jsonschema import validate

from src.GUI.Util.CONSTANTS import DEVICES_SCHEMA_FILE_NAME


class HardwareManager:
    def __init__(self, hardware_config):
        """
        Initializes the hardware manager with a list of drivers and configured hardware devices
        :param hardware_config:
            The .json file which holds the hardware configuration
        """
        self._hardware_objects = {}

        with open(hardware_config) as f:
            config = json.load(f)
        with open(DEVICES_SCHEMA_FILE_NAME) as f:
            schema = json.load(f)
        validate(instance=config, schema=schema)

        for key in config:
            self._hardware_objects[key] = HardwareModel(**config[key])

    def get_hardware_object(self, name):
        """
        :param name:
            The name of the hardware in the configuration file
        :return:
            A Hardware object representing the configuration of the hardware with the given name
        """
        return self._hardware_objects[name]

    def get_all_hardware_names(self):
        """
        :return:
            A list of all of the names of hardware devices in the configuration file provided on initialization
        """
        return list(self._hardware_objects.keys())
