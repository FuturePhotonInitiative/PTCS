import wx
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS

class BuildExperimentsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.experimentsBox = wx.StaticBox(self)
        self.scriptsBox = wx.StaticBox(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.scriptsBox, CONSTANTS.BUILD_SCRIPT_PANEL_PROPORTION, wx.EXPAND)
        sizer.Add(self.experimentsBox, CONSTANTS.BUILD_PANEL_PROPORTION, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Layout()
