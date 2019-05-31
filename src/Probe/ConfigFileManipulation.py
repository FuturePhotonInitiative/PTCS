import json
import os
import sys


class ConfigFileManipulation:
    def __init__(self, file_name):
        with open(file_name) as f:
            self.config = json.load(f)

    def check_validity(self, file_locations):
        """
        Checks the config file to ensure that information is properly input in json configuration
        This is specific to the current configuration file and will need to change when the file changes
        :param file_locations, locations for specific directories
        :return: problems, array of things wrong with the configuration file
        """
        problems = []
        devices = self.config["Devices"]
        experiments = self.config["Experiment"]
        with open(file_locations["Hardware_Config"]) as d:
            hardware_manager = json.load(d)
        if "Name" not in self.config.keys():
            problems.append("Name : does not exist in configuration file")
        for fil in ["Script_Root", "Driver_Root"]:
            if fil not in file_locations.keys():
                problems.append("Files-" + fil + " : does not exist in configuration file")
            else:
                if not os.path.exists(file_locations[fil]):
                    problems.append("Files-" + fil + " : path does not exist")
        for device in devices:
            if device not in hardware_manager.keys():
                problems.append("Devices-" + device + " : device not found in hardware manager. Check spelling.")
            else:
                for key in hardware_manager[device].keys():
                    if key not in ["Driver", "Type", "Default"]:
                        problems.append(device + "-" + key + " : improper structure of json hardware manager file.")
        for experiment in experiments:
            for exp in ["Type", "Source", "Order"]:
                if exp not in experiment.keys():
                    problems.append("Experiment-" + exp + " : does not exist in configuration file")

        if len(problems) is not 0:
            print "ABORTING! Configuration file not formatted correctly."
            for problem in problems:
                print problem
            sys.exit(1)

    def initialize_data(self, data_map):
        """
        Initializes optional Data section of the JSON config into the data map for the tasks
        :param data_map: The dictionary to store data between tasks
        :param json_file: The JSON config object
        :return: None
        """
        data_section = self.config.get('Data', None)
        if data_section is None:
            return
        data_map['Data']['Initial'] = {}
        for key in data_section.keys():
            data_map['Data']['Initial'][key] = data_section[key]
        return

    def extract_scripts(self, file_locations):
        """
        Extracts the scripts from the JSON config and stages them for execution. This will put the scripts in an ordered
            list where each element is a list of tasks to be spawned in parallel
        :param json_file: The JSON config object
        :param json_locations: The JSON Files object with standard file directories
        :return: The list of staged task lists
        """
        scripts_root = str(file_locations['Script_Root'])
        available_scripts = os.listdir(scripts_root)
        available_scripts = [i for i in available_scripts if not (i == '__init__.py' or i[-3:] != '.py')]

        scripts = {}
        for item in [i for i in self.config['Experiment'] if i['Type'] == "PY_SCRIPT"]:

            if str(item['Source']) not in available_scripts:
                sys.exit("Required script \'" + item['Source'] + "\' not found")

            if item['Order'] in scripts.keys():
                scripts[item['Order']].append(item['Source'])
            else:
                scripts[item['Order']] = [item['Source']]
        sorted_scripts = []
        for key in sorted(scripts.keys()):
            sorted_scripts.append(scripts[key])
        return sorted_scripts
