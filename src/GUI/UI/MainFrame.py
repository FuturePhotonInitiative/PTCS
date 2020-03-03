import wx

from .ExperimentResults.ExperimentResultsPage import ExperimentResultsPage
from .Hardware.HardwarePage import HardwarePage
from .Queue.QueuePage import QueuePage

from src.GUI.Util import CONSTANTS
from src.GUI.UI.TestBuild.TestBuildPage import TestBuildPage
from src.GUI.Util import Globals


class MainFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, CONSTANTS.MAIN_PAGE_TITLE, size=CONSTANTS.PAGE_SIZE)
        self.panel = wx.Panel(self)
        self.notebook = wx.Notebook(self.panel)
        # self.notebook.SetTabSize()

        self.timer = wx.Timer(self)
        self.queue_page = QueuePage(self.notebook)
        self.hardware_page = HardwarePage(self.notebook)
        # self.build_experiments_page = BuildExperimentsPage(self.notebook)
        self.experiment_results_page = ExperimentResultsPage(self.notebook)
        self.test_build_page = TestBuildPage(self.notebook)

        self.notebook.AddPage(self.queue_page, CONSTANTS.QUEUE_PAGE_NAME)
        self.notebook.AddPage(self.experiment_results_page, CONSTANTS.RESULTS_PAGE_NAME)
        self.notebook.AddPage(self.hardware_page, CONSTANTS.HARDWARE_PAGE_NAME)
        self.notebook.AddPage(self.test_build_page, CONSTANTS.TEST_BUILD_PAGE_NAME)
        # self.notebook.AddPage(self.build_experiments_page, CONSTANTS.BUILD_EXPERIMENTS_PAGE_NAME)

        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        sizer.Layout()
        # self.fix_tab_size(None)
        self.Bind(wx.EVT_SIZE, self.fix_tab_size)

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
