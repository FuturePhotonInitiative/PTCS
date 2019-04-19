import wx
from src.GUI.UI.ExperimentResults.ExperimentResultsPage import ExperimentResultsPage
from src.GUI.UI.Hardware.HardwarePage import HardwarePage
from src.GUI.UI.BuildExperiment.BuildExperimentPage import BuildExperimentsPage
from src.GUI.UI.Queue.QueuePage import QueuePage
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS
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
        self.build_experiments_page = BuildExperimentsPage(self.notebook)
        self.experiment_results_page = ExperimentResultsPage(self.notebook)

        self.notebook.AddPage(self.queue_page, CONSTANTS.QUEUE_PAGE_NAME)
        self.notebook.AddPage(HardwarePage(self.notebook), CONSTANTS.HARDWARE_PAGE_NAME)
        self.notebook.AddPage(BuildExperimentsPage(self.notebook), CONSTANTS.BUILD_EXPERIMENTS_PAGE_NAME)
        self.notebook.AddPage(ExperimentResultsPage(self.notebook), CONSTANTS.RESULTS_PAGE_NAME)


        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        sizer.Layout()
        # self.fix_tab_size(None)
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
                                         CONSTANTS.BUILD_EXPERIMENTS_PAGE_NAME +
                                         CONSTANTS.RESULTS_PAGE_NAME)
        size = (self.GetSize()[0] - width - CONSTANTS.SPACE_SIZE * (self.notebook.GetPageCount() + 1) ) / (self.notebook.GetPageCount() * 2)
        self.notebook.SetPadding(wx.Size(size, 3))

    def run_page_update(self, event):
        # print "ding"
        UI_controller = Globals.systemConfigManager.get_ui_controller()
        if UI_controller:
            UI_controller.fix_control_list()
            UI_controller.rebuild_all_pages()

