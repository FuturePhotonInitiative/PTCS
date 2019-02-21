import json
from ExperimentScriptModel import ExperimentScript


class Experiment:

    def __init__(self, config_file, dependencies, priority):
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
        with open(config_file) as config:
            self.config_dict = json.load(config)
        self.scripts = []
        for s in self.config_dict['Experiment']:
            self.scripts.append(ExperimentScript(s))
        self.sort_scripts(0, len(self.scripts)-1)
        self.dependencies = dependencies
        self.priority = priority

    def sort_scripts(self, left_idx, right_idx):
        """
        Quicksorts the experiments in the list according to their 'Order' attribute in the experiment's json file.
        (A bubble sort probably would have sufficed, but I really wanted to flex my algorithm muscles)
        This function is called when the experiment object is constructed, so there's no need to call it again
        :param left_idx:
            The left index of the sublist to sort
        :param right_idx:
            The right index of the sublist to sort
        :return:
            None
        """
        if left_idx == right_idx:
            return
        pivot = self.scripts[left_idx]
        pivots = []
        tmp_list = self.scripts[:]
        left_insert = left_idx
        right_insert = right_idx
        for i in range(left_idx, right_idx + 1):
            if self.scripts[i].order < pivot.order:
                tmp_list[left_insert] = self.scripts[i]
                left_insert = left_insert + 1
            elif self.scripts[i].order > pivot.order:
                tmp_list[right_insert] = self.scripts[i]
                right_insert = right_insert - 1
            else:
                pivots.append(self.scripts[i])
        tmp_list[left_insert:right_insert+1] = pivots
        self.scripts = tmp_list
        self.sort_scripts(left_idx, left_insert - 1)
        self.sort_scripts(right_insert + 1, right_idx)

    def get_data_value(self, data_key):
        """
        Get a value from the "Data" section of the Experiment's configuration JSON
        :param data_key:
            The name of the value to get
        :return:
            The value associated with the given key
        """
        return self.config_dict["Data"][data_key]

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
        self.config_dict["Data"][data_key] = data_value

    def get_data_keys(self):
        """
        :return:
            All of the keys currently set in the "Data" section of the experiment's configuration
        """
        return self.config_dict["Data"].keys()

    def get_scripts(self):
        """
        :return:
            A sorted list of ExperimentScript objects, representing the scripts defined in the experiment's
            configuration.  The Scripts are sorted based on their "Order" value
        """
        return self.scripts

    def get_ith_script(self, i):
        """
        :param i:
            The index of the script to return (0-based)
        :return:
            The ith experiment script when the scripts are sorted by their "Order"
        """
        return self.scripts[i]

    def get_name(self):
        """
        :return:
            The name of this experiment as defined in the configuration
        """
        return self.config_dict["Name"]

    def get_required_devices(self):
        """
        :return:
            A list of device names required by this experiment.
            The names should be defined in the system's hardware configuration
        """
        return self.config_dict['Requires']['Devices']

    def get_required_files(self):
        """
        :return:
            A dictionary of the files defined in the Experiment's Requires->Files configuration section
        """
        return self.config_dict['Requires']['Files']

    def get_script_root(self):
        """
        :return:
            The value of "Script_Root" defined in the configuration.
        """
        return self.get_required_files()['Script_Root']

    # TODO this value should be moved to the system configuration rather than on an experiment by experiment basis
    def get_driver_root(self):
        """
        :return:
            The value of "Driver_Root" as defined in the configuration.
        """
        return self.get_required_files()['Driver_Root']

    def get_results_root(self):
        """
        :return:
            The value of "Results_Root" as defined in the configuration.
        """
        return self.get_required_files()['Results_Root']

    """ 
    TODO this will almost certainly be moved out of the experiment configuration files
    and into the system configuration files
    """
    def get_hardware_config(self):
        return self.get_required_files()['Hardware_Config']

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
        with open(filename, 'w') as file:
            json.dump(self.config_dict, file, indent=4 if pretty_print else None)
