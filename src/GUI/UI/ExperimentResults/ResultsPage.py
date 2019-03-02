import wx
import ExperimentListPanel


class ResultsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.ExperimentListBox = ExperimentListPanel.ExperimentListPanel(self)
        self.ResultsListBox = wx.StaticBox(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.ExperimentListBox, 1, wx.EXPAND)
        sizer.Add(self.ResultsListBox, 1, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Layout()
