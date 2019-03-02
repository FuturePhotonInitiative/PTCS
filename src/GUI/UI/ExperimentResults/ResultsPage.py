import wx
from ExperimentListPanel import ExperimentListPanel
from ResultsFileListPanel import ResultsFileListPanel


class ResultsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.ExperimentListBox = ExperimentListPanel(self)
        self.ResultsListBox = ResultsFileListPanel(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.ExperimentListBox, 1, wx.EXPAND)
        sizer.Add(self.ResultsListBox, 1, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Layout()
