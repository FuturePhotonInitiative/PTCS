import wx

from ExperimentResults.ExperimentResultsPage import ExperimentResultsPage
from Hardware.HardwarePage import HardwarePage
from Queue.QueuePage import QueuePage
from TestBuild.TestBuildPage import TestBuildPage

from src.GUI.Application.HardwareManager import HardwareManager
from src.GUI.Application.ExperimentsManager import ExperimentsManager
from src.GUI.Application.ResultsManager import ResultsManager
from src.GUI.Application.QueueManager import QueueManager

from src.GUI.Util import CONSTANTS
from src.GUI.Application.UIController import UIController


class MainFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, CONSTANTS.MAIN_PAGE_TITLE, size=CONSTANTS.PAGE_SIZE)\

        hardware_manager = HardwareManager(CONSTANTS.DEVICES_CONFIG, CONSTANTS.DRIVERS_DIR)
        experiments_manager = ExperimentsManager(CONSTANTS.CONFIGS, CONSTANTS.SCRIPTS_DIR)
        results_manager = ResultsManager(CONSTANTS.RESULTS_DIR, CONSTANTS.RESULTS_CONFIG_DIR)
        queue_manager = QueueManager(CONSTANTS.TEMP_DIR, results_manager)

        self.panel = wx.Panel(self)
        self.notebook = wx.Notebook(self.panel)

        self.ui_controller = UIController(self)

        self.queue_page = QueuePage(self.notebook, experiments_manager, queue_manager)
        self.hardware_page = HardwarePage(self.notebook, hardware_manager)
        self.experiment_results_page = ExperimentResultsPage(self.notebook, results_manager)
        self.test_build_page = TestBuildPage(self.notebook, hardware_manager)

        self.timer = wx.Timer(self)
        self.queue_page.set_up_ui_control(self.ui_controller)
        self.hardware_page.set_up_ui_control(self.ui_controller)
        self.experiment_results_page.set_up_ui_control(self.ui_controller)

        self.notebook.AddPage(self.queue_page, CONSTANTS.QUEUE_PAGE_NAME)
        self.notebook.AddPage(self.experiment_results_page, CONSTANTS.RESULTS_PAGE_NAME)
        self.notebook.AddPage(self.hardware_page, CONSTANTS.HARDWARE_PAGE_NAME)
        self.notebook.AddPage(self.test_build_page, CONSTANTS.TEST_BUILD_PAGE_NAME)

        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        sizer.Layout()
        self.Bind(wx.EVT_SIZE, self.fix_tab_size)
        self.Bind(wx.EVT_TIMER, self.run_page_update, self.timer)
        self.timer.Start(500)

    def fix_tab_size(self, event):
        event.Skip()
        f = self.GetFont()
        dc = wx.WindowDC(self)
        dc.SetFont(f)
        width, height = dc.GetTextExtent(CONSTANTS.QUEUE_PAGE_NAME +
                                         CONSTANTS.HARDWARE_PAGE_NAME +
                                         CONSTANTS.RESULTS_PAGE_NAME +
                                         CONSTANTS.TEST_BUILD_PAGE_NAME)
        size = (self.GetSize()[0] - width - CONSTANTS.SPACE_SIZE * (self.notebook.GetPageCount() + 1)) / (self.notebook.GetPageCount() * 2)
        self.notebook.SetPadding(wx.Size(size, 3))

    def run_page_update(self, event):
        self.ui_controller.fix_control_list()
        self.ui_controller.rebuild_all_pages()
