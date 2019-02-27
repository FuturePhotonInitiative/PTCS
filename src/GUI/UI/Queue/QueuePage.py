import wx
from src.GUI.UI.Queue.QueuePanel import QueuePanel
from src.GUI.UI.Queue.ExperimentControlPanel import ExperimentControlPanel


class QueuePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.queueBox = QueuePanel(self)
        self.controlBox = ExperimentControlPanel(self, None)

        # self.queueBox.SetForegroundColour(wx.WHITE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.controlBox, 1, wx.EXPAND | wx.ALL)
        sizer.Add(self.queueBox, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Layout()

    def get_experiments(self):
        return []