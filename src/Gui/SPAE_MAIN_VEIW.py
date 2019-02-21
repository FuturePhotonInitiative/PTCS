import wx
from ResultsPage import ResultsPage
from HardwarePage import HardwarePage
from BuildExperimentPage import BuildExperimentsPage
from QueuePage import QueuePage

MAIN_PAGE_TITLE = "Prober Control"
PAGE_SIZE = (900, 500)
QUEUE_PAGE_NAME = "Queue"
HARDWARE_PAGE_NAME = "Hardware"
BUILD_EXPERIMENTS_PAGE_NAME = "Build"
RESULTS_PAGE_NAME = "Results"


class MainFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, MAIN_PAGE_TITLE, size=PAGE_SIZE)
        self.panel = wx.Panel(self)
        self.notebook = wx.Notebook(self.panel)
        # self.notebook.SetTabSize()
        self.notebook.AddPage(QueuePage(self.notebook), QUEUE_PAGE_NAME)
        self.notebook.AddPage(HardwarePage(self.notebook), HARDWARE_PAGE_NAME)
        self.notebook.AddPage(BuildExperimentsPage(self.notebook), BUILD_EXPERIMENTS_PAGE_NAME)
        self.notebook.AddPage(ResultsPage(self.notebook), RESULTS_PAGE_NAME)

        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        sizer.Layout()


if __name__ == '__main__':
    app=wx.App()
    frame = MainFrame(None, -1)
    frame.Show()
    app.MainLoop()