import json
from HardwareManager import HardwareManager
from QueueManager import QueueManager
from ExperimentsManager import ExperimentsManager
from ResultsManager import ResultsManager


class SystemConfigManager:
    def __init__(self, files_path):
        self.file_locations = {}
        with open(files_path) as config_file:
            self.file_locations = json.load(config_file)
        self.experiments_manager = None
        self.results_manager = None
        self.queue_manager = None
        self.hardware_manager = None

    def get_hardware_manager(self):
        if self.hardware_manager is None:
            self.hardware_manager = \
                HardwareManager(self.file_locations["Hardware_Config"], self.file_locations["Driver_Root"])
        return self.hardware_manager

    def get_experiments_manager(self):
        if self.experiments_manager is None:
            self.experiments_manager = \
                ExperimentsManager(self.file_locations["Experiment_Roots"], self.file_locations["Script_Root"])
        return self.experiments_manager

    def get_queue_manager(self):
        if self.queue_manager is None:
            self.queue_manager = QueueManager()
        return self.queue_manager

    def get_results_manager(self):
        if self.results_manager is None:
            self.results_manager = ResultsManager(self.file_locations["Results_Root"])
        return self.results_manager
