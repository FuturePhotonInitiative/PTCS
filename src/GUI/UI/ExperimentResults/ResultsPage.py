import wx
from ExperimentListPanel import ExperimentListPanel
from ResultsFileListPanel import ResultsFileListPanel
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS


class ResultsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.ExperimentListBox = ExperimentListPanel(self)
        self.ResultsListBox = ResultsFileListPanel(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.ExperimentListBox, CONSTANTS.RESULTS_EXPERIMENT_PANEL_PROPORTION, wx.EXPAND)
        sizer.Add(self.ResultsListBox, CONSTANTS.RESULTS_FILE_PANEL_PROPORTION, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Layout()
