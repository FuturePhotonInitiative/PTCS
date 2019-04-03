import json
from HardwareManager import HardwareManager
from QueueManager import QueueManager
from ExperimentsManager import ExperimentsManager
from ResultsManager import ResultsManager
from src.GUI.Util import GUI_CONSTANTS


class SystemConfigManager:
    def __init__(self, files_path):
        """
        Create a new SystemConfigurationManager based on the "Files" configuration provided
        :param files_path:
            The path to the Files.json file which describes the location of all of the other required configuration
            files.
        """

        self.files_path = files_path

        self.file_locations = {}
        with open(files_path) as config_file:
            self.file_locations = json.load(config_file)

        files_path = files_path[0:files_path.rfind("/")]
        for config in self.file_locations:
            # TODO only relative paths should be relative to the Files.json file: fix this
            # TODO test this
            if type(self.file_locations[config]) == list:
                for i in range(len(self.file_locations[config])):
                    if self.file_locations[config][i][0] != '/':
                        self.file_locations[config][i] = files_path + "/" + self.file_locations[config][i]
            elif self.file_locations[config][0] != '/':
                self.file_locations[config] = files_path + "/" + self.file_locations[config]
        self.experiments_manager = None
        self.results_manager = None
        self.queue_manager = None
        self.hardware_manager = None

    def get_hardware_manager(self):
        """
        Create a new or return an existing HardwareManager based on the Hardware configuration files pointed to by
        the files_path referenced in this SystemConfigManager's constructor
        :return:
            A new HardwareManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.hardware_manager is None:
            self.hardware_manager = \
                HardwareManager(self.file_locations["Hardware_Config"], self.file_locations["Driver_Root"], self)
        return self.hardware_manager

    def get_experiments_manager(self):
        """
        Create a new or return an existing ExperimentsManager based on the Experiment_Roots and Script_Root directories
        pointed to by the files_path referenced in this SystemConfigManager's constructor
        :return:
            A new ExperimentsManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.experiments_manager is None:
            self.experiments_manager = \
                ExperimentsManager(self.file_locations["Experiment_Roots"], self.file_locations["Script_Root"], self)
        return self.experiments_manager

    def get_queue_manager(self):
        """
        Create a new or return an existing QueueManager object
        :return:
            A new QueueManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.queue_manager is None:
            self.queue_manager = QueueManager(GUI_CONSTANTS.WORKING_DIRECTORY, self)
        return self.queue_manager

    def get_results_manager(self):
        """
        Create a new or return an existing ResultsManager based on the Results_Root directory
        pointed to by the files_path referenced in this SystemConfigManager's constructor
        :return:
            A new ResultsManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.results_manager is None:
            self.results_manager = ResultsManager(self.file_locations["Results_Root"],
                                                  self.file_locations["Results_Config_Root"], self)
        return self.results_manager

    def set_script_root(self, new_root):
        self.file_locations['Script_Root'] = new_root

    def set_driver_root(self, new_root):
        self.file_locations['Driver_Root'] = new_root

    def set_results_root(self, new_root):
        self.file_locations['Results_Root'] = new_root

    def set_hardware_config_location(self, new_location):
        self.file_locations['Hardware_Config'] = new_location

    def add_experiment_root(self, new_root):
        self.file_locations["Experiment_Roots"].append(new_root)

    def remove_experiment_root(self, root_to_remove):
        # TODO this causes an error if the root is not already present
        self.file_locations['Experiment_Roots'].remove(root_to_remove)

    # TODO commit to json function
    """
    Requirements:
        -Must make paths relative to the Files.json file or otherwise absolute
        -Must write the current system configuration to a json file
        -Must provide an option to write to a different location (Default argument)
    """
