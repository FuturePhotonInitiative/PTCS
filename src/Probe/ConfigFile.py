import json
import os
import sys

from src.GUI.Util import CONSTANTS


class ConfigFile:
    def __init__(self, file_name):
        with open(file_name) as f:
            self.config = json.load(f)

    def check_validity(self):
        """
        Checks the config file to ensure that information is properly input in json configuration
        This is specific to the current configuration file and will need to change when the file changes
        :return: problems, array of things wrong with the configuration file
        """
        problems = []
        devices = self.config["Devices"]
        experiments = self.config["Experiment"]
        with open(CONSTANTS.DEVICES_CONFIG) as d:
            hardware_manager = json.load(d)
        if "Name" not in self.config.keys():
            problems.append("Name : does not exist in configuration file")
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
        :return: None
        """
        data_section = self.config.get('Data', None)
        if data_section is None:
            return
        data_map['Data']['Initial'] = {}
        for key in data_section.keys():
            data_map['Data']['Initial'][key] = data_section[key]
        return

    def extract_scripts(self):
        """
        Extracts the scripts from the JSON config and stages them for execution. This will put the scripts in an ordered
            list where each element is a list of tasks to be spawned in parallel
        :return: The list of staged task lists
        """
        available_scripts = os.listdir(CONSTANTS.SCRIPTS_DIR)
        available_scripts = [i for i in available_scripts if not (i == '__init__.py' or i[-3:] != '.py')]

        scripts = {}
        for item in [i for i in self.config['Experiment'] if i['Type'] == "PY_SCRIPT"]:
            if str(item['Source']) not in available_scripts:
                print("Required script \'" + item['Source'] + "\' not found")
                sys.exit(1)

            if item['Order'] in scripts.keys():
                scripts[item['Order']].append(item['Source'])
            else:
                scripts[item['Order']] = [item['Source']]
        sorted_scripts = []
        for key in sorted(scripts.keys()):
            sorted_scripts.append(scripts[key])
        return sorted_scripts
