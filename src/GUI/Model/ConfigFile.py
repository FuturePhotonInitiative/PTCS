import json

from jsonschema import validate

from src.GUI.Model.ExperimentScriptModel import ExperimentScript
from copy import deepcopy


class ConfigFile:
    """
    This is the model for a config file. Whenever a config file is manipulated by the program,
    it loads the config file into an object by calling from_json_file.
    The object is then possibly manipulated and then possibly dumped to a file
    """

    def __init__(self, name, experiment=None, devices=None, data=None, tcl=None):
        if experiment is None:
            experiment = []
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
        """
        Opens the config file and the schema file, validates the config file against the schema file,
        and creates a class based on the dict read in from the config file
        :param file_name: the config file's name
        :param schema_name: the schema file's name
        :return: an instance of this class with the data from the config file
        """
        with open(file_name) as f:
            config = json.load(f)
        with open(schema_name) as f:
            schema = json.load(f)
        validate(instance=config, schema=schema)
        return cls(**config)

    def copy(self):
        return ConfigFile(**self.to_dict())

    def to_dict(self):
        """
        Makes a deep copy of this class and returns its dictionary representation
        with each entry with a null or empty value removed
        """
        copy = deepcopy(self)
        copy.experiment = [i.__dict__ for i in self.experiment]
        dct = copy.__dict__
        for item in dct.keys():
            if not dct[item]:
                del dct[item]
        return dct

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
