import wx
from src.GUI.Util import GUI_CONSTANTS
from HardwareListPanel import HardwareListPanel

import src.GUI.Util.GUI_CONSTANTS as CONSTANTS

class HardwarePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.hardwareBox = HardwareListPanel(self)
        self.controlBox = wx.StaticBox(self)

        self.hardwareBox.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.hardwareBox.SetLabelText(GUI_CONSTANTS.HARDWARE_PANEL_NAME)
        self.hardwareBox.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_side = wx.BoxSizer(wx.VERTICAL)
        right_side.Add(wx.StaticText(self, label="Available Hardware"), CONSTANTS.QUEUE_LABEL_PROPORTION, wx.TOP)
        right_side.Add(self.hardwareBox, 1, wx.EXPAND | wx.ALL)
        sizer.Add(self.controlBox, CONSTANTS.HARDWARE_CONTROL_PANEL_PROPORTION, wx.EXPAND, CONSTANTS.LIST_PANEL_MARGIN)
        sizer.Add(right_side, CONSTANTS.HARDWARE_PANEL_PROPORTION, wx.EXPAND, CONSTANTS.LIST_PANEL_MARGIN)

        self.SetSizer(sizer)
        sizer.Layout()
