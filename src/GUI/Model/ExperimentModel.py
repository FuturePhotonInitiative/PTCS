import json
from src.GUI.Model.ConfigFile import ConfigFile
from src.GUI.Util.CONSTANTS import JSON_SCHEMA_FILE_NAME


class Experiment:

    def __init__(self, config_file, dependencies=None, priority=1):
        """
        Construct a new Experiment object.
        :param config_file:
            The experiment's configuration JSON file, from which its properties will be read
        :param dependencies:
            A list of experiment objects defining the experiments this experiment depends on
        :param priority:
            The integer priority of the experiment.  In general, higher priority experiments should run before lower
            priority experiments, but only after all of their dependencies have run.
        """
        self.config_file_name = config_file
        self.config = ConfigFile.from_json_file(config_file, JSON_SCHEMA_FILE_NAME)
        self.dependencies = dependencies
        self.priority = priority
        if self.config.tcl:
            self.tcl_file = self.config.tcl

    def copy(self):
        return Experiment(self.config_file_name, dependencies=self.dependencies, priority=self.priority)

    def __str__(self):
        return self.get_name()

    def get_data_value(self, data_key):
        """
        Get a value from the "Data" section of the Experiment's configuration JSON
        :param data_key:
            The name of the value to get
        :return:
            The value associated with the given key
        """
        return self.config.data[data_key]

    def set_data_value(self, data_key, data_value):
        """
        Set a the value of a variable in the data section in the configuration of the experiment
        :param data_key:
            The name of the variable to set.
        :param data_value:
            The value to set the variable to
        :return:
            None
        """
        self.config.data[data_key] = data_value

    def get_data_keys(self):
        """
        :return:
            All of the keys currently set in the "Data" section of the experiment's configuration
        """
        if self.config.data:
            return self.config.data.keys()
        else:
            return []

    def get_scripts(self):
        """
        :return:
            A sorted list of ExperimentScript objects, representing the scripts defined in the experiment's
            configuration.  The Scripts are sorted based on their "Order" value
        """
        return self.config.scripts

    def get_ith_script(self, i):
        """
        :param i:
            The index of the script to return (0-based)
        :return:
            The ith experiment script when the scripts are sorted by their "Order"
        """
        return self.config.scripts[i]

    def get_name(self):
        """
        :return:
            The name of this experiment as defined in the configuration
        """
        return self.config.name

    def export_to_json(self, filename, pretty_print=True):
        """
        Write the configuration stored in this Experiment object to a json formatted file
        :param filename:
            The name of the file to write to.  WARNING: The specified file will be overwritten
        :param pretty_print:
            If true, print the json with indentation, otherwise keep the JSON compact
        :return:
        None
        """
        with open(filename, 'w') as f:
            json.dump(self.config.to_dict(), f, indent=4 if pretty_print else None)
