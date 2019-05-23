import json
from src.GUI.Model.ExperimentScriptModel import ExperimentScript


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
        with open(config_file) as config:
            self.config_dict = json.load(config)
        self.scripts = []
        if self.config_dict.get('Experiment', None) is not None:
            for s in self.config_dict['Experiment']:
                self.scripts.append(ExperimentScript(s))
        self.scripts = sorted(self.scripts, key=lambda elem: elem.order)
        self.dependencies = dependencies
        self.priority = priority
        if self.config_dict.get('Tcl', None) is not None:
            self.tcl_file = self.config_dict['Tcl']

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


if __name__ == "__main__":
    test = Experiment("../../Configs/Threshold_With_Hardware.json", None, 12)
    print (test.get_data_value("Start_Voltage"))
    print (test.get_data_value("Final_Voltage"))
    print (test.get_data_value("Step_Voltage"))
    test.set_data_value("Start_Voltage", 10.0)
    test.export_to_json("tmp.json", True)
