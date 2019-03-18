import json
import os


class HardwareManager:
    def __init__(self, hardware_config, driver_root):
        self.hardware_objects = {}
        self.drivers = []
        with open(hardware_config) as config_file:
            self.hardware_objects = json.load(config_file)
        self.drivers = os.listdir(driver_root)
