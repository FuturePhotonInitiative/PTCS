import json
import os

from jsonschema import validate

from src.GUI.Model.ExperimentScriptModel import ExperimentScript
from src.GUI.Util import CONSTANTS
from copy import deepcopy


class ConfigFile:

    def __init__(self, name, experiment, devices=None, data=None, tcl=None):
        self.name = name

        self.experiment = []
        for script in experiment:
            self.experiment.append(ExperimentScript(script))
        self.experiment = sorted(self.experiment, key=lambda elem: elem.order)

        self.devices = devices
        self.data = data

        self.tcl = tcl

    @classmethod
    def from_json_file(cls, file_name, schema_name):
        with open(file_name) as f:
            config = json.load(f)
        with open(schema_name) as f:
            schema = json.load(f)
        validate(instance=config, schema=schema)
        return cls(**config)

    def to_dict(self):
        dct = deepcopy(self)
        dct.experiment = [i.__dict__ for i in self.experiment]
        return dct.__dict__

    def initialize_data(self, data_map):
        """
        Initializes optional Data section of the JSON config into the data map for the tasks
        :param data_map: The dictionary to store data between tasks
        :return: None
        """
        if self.data:
            data_map['Data']['Initial'] = {}
            for key in self.data.keys():
                data_map['Data']['Initial'][key] = self.data[key]


if __name__ == "__main__":
    # testing to make sure validation works out correctly
    test2 = ConfigFile.from_json_file(os.path.join(CONSTANTS.CONFIGS, "test2"), CONSTANTS.JSON_SCHEMA_FILE_NAME)
    print(test2.__dict__)



