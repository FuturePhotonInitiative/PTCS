import wx
from ResultsPage import ResultsPage
from HardwarePage import HardwarePage
from BuildExperimentPage import BuildExperimentsPage
from QueuePage import QueuePage



def addSpaces(string, count):
    for i in range(0,int(count)):
        if i % 2 == 0:
            string = " " + string
        else:
            string = string + " "
    return string


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
        # self.fixTabSize(None)
        self.Bind(wx.EVT_SIZE, self.fixTabSize)

    def fixTabSize(self, event):
        event.Skip()
        f = self.GetFont()
        dc = wx.WindowDC(self)
        dc.SetFont(f)
        width, height = dc.GetTextExtent(QUEUE_PAGE_NAME +
                                         HARDWARE_PAGE_NAME +
                                         BUILD_EXPERIMENTS_PAGE_NAME +
                                         RESULTS_PAGE_NAME)
        size = (self.GetSize()[0] - width - SPACE_SIZE * (self.notebook.GetPageCount() + 1) ) / (self.notebook.GetPageCount() * 2)
        self.notebook.SetPadding(wx.Size(size, 3))

if __name__ == '__main__':
    app=wx.App()
    frame = MainFrame(None, -1)
    frame.Show()
    app.MainLoop()

