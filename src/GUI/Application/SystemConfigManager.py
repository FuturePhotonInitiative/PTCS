import json
from HardwareManager import HardwareManager
from QueueManager import QueueManager
from ExperimentsManager import ExperimentsManager
from ResultsManager import ResultsManager


class SystemConfigManager:
    def __init__(self, files_path):
        """
        Create a new SystemConfigurationManager based on the "Files" configuration provided
        :param files_path:
            The path to the Files.json file which describes the location of all of the other required configuration
            files.
        """
        self.file_locations = {}
        with open(files_path) as config_file:
            self.file_locations = json.load(config_file)
        for config in self.file_locations:
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
                HardwareManager(self.file_locations["Hardware_Config"], self.file_locations["Driver_Root"])
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
                ExperimentsManager(self.file_locations["Experiment_Roots"], self.file_locations["Script_Root"])
        return self.experiments_manager

    def get_queue_manager(self):
        """
        Create a new or return an existing QueueManager object
        :return:
            A new QueueManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.queue_manager is None:
            self.queue_manager = QueueManager()
        return self.queue_manager

    def get_results_manager(self):
        """
        Create a new or return an existing ResultsManager based on the Results_Root directory
        pointed to by the files_path referenced in this SystemConfigManager's constructor
        :return:
            A new ResultsManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.results_manager is None:
            self.results_manager = ResultsManager(self.file_locations["Results_Root"])
        return self.results_manager
