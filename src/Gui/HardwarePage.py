import wx
import GUI_CONSTANTS

class HardwarePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.hardwareBox = wx.StaticBox(self)
        self.controlBox = wx.StaticBox(self)

        self.hardwareBox.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.hardwareBox.SetLabelText(GUI_CONSTANTS.HARDWARE_PANEL_NAME)
        self.hardwareBox.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.controlBox, 1, wx.EXPAND)
        sizer.Add(self.hardwareBox, 3, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Layout()
