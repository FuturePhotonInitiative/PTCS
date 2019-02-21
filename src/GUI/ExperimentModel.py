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
        return self.config_dict["Data"][data_key]

    def set_data_value(self, data_key, data_value):
        self.config_dict["Data"][data_key] = data_value

    def get_data_keys(self):
        return self.config_dict["Data"].keys()

    def get_scripts(self):
        return self.scripts

    def get_ith_script(self, i):
        return self.scripts[i]

    def get_name(self):
        return self.config_dict["Name"]

    def get_required_devices(self):
        return self.config_dict['Requires']['Devices']

    def get_required_files(self):
        return self.config_dict['Requires']['Files']

    def get_script_root(self):
        return self.get_required_files()['Script_Root']

    def get_driver_root(self):
        return self.get_required_files()['Driver_Root']

    def get_results_root(self):
        return self.get_required_files()['Results_Root']

    """ 
    TODO this will almost certainly be moved out of the experiment configuration files
    and into the system configuration files
    """
    def get_hardware_config(self):
        return self.get_required_files()['Hardware_Config']

