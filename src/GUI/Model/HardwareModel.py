import os
import json


class HardwareModel:

    def __init__(self, system_config):
        self.system_config_files = system_config
        self.system_config = {}
        for sysfile in self.system_config_files:
            with open(sysfile) as f:
                self.system_config[os.path.basename(sysfile).replace('.json', "")] = json.load(f)

        self.hardware = self.system_config["Devices"]
        # print self.get_hardware_names()

    def get_hardware_names(self):
        return self.hardware.keys()

    def get_configured_hardware(self):
        # TODO
        pass

    def get_driver_directory(self):
        return self.system_config['Files']['Driver_Root']
