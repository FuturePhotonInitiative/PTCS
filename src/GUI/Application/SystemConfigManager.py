from .HardwareManager import HardwareManager
from .QueueManager import QueueManager
from .ExperimentsManager import ExperimentsManager
from .ResultsManager import ResultsManager
from src.GUI.Application.UIController import UIController
from src.GUI.Util import CONSTANTS


class SystemConfigManager:
    def __init__(self):
        """
        """
        self.mainframe = None
        self.ui_controller = None
        self.experiments_manager = None
        self.results_manager = None
        self.queue_manager = None
        self.hardware_manager = None

    def get_ui_controller(self):
        """
        Create a new or return an existing HardwareManager based on the Hardware configuration files pointed to by
        the files_path referenced in this SystemConfigManager's constructor
        :return:
            A new HardwareManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.ui_controller is None and self.mainframe is not None:
            self.ui_controller = UIController(self.mainframe)
        return self.ui_controller

    def get_hardware_manager(self):
        """
        Create a new or return an existing HardwareManager based on the Hardware configuration files pointed to by
        the files_path referenced in this SystemConfigManager's constructor
        :return:
            A new HardwareManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.hardware_manager is None:
            self.hardware_manager = \
                HardwareManager(CONSTANTS.DEVICES_CONFIG, CONSTANTS.DRIVERS_DIR)
        return self.hardware_manager

    def get_experiments_manager(self):
        """
        Create a new or return an existing ExperimentsManager
        :return:
            A new ExperimentsManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.experiments_manager is None:
            self.experiments_manager = ExperimentsManager(CONSTANTS.CONFIGS, CONSTANTS.SCRIPTS_DIR)
        return self.experiments_manager

    def get_queue_manager(self):
        """
        Create a new or return an existing QueueManager object
        :return:
            A new QueueManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.queue_manager is None:
            self.queue_manager = QueueManager(CONSTANTS.TEMP_DIR, self)
        return self.queue_manager

    def get_results_manager(self):
        """
        Create a new or return an existing ResultsManager
        :return:
            A new ResultsManager object if one has not already been created by this class, an existing on otherwise.
        """
        if self.results_manager is None:
            self.results_manager = ResultsManager(CONSTANTS.RESULTS_DIR, CONSTANTS.RESULTS_CONFIG_DIR)
        return self.results_manager
