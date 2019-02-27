import wx
import Constants

class HardwarePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.hardwareBox = wx.StaticBox(self)
        self.controlBox = wx.StaticBox(self)

        self.hardwareBox.SetBackgroundColour(Constants.HARDWARE_PANEL_COLOR)
        self.hardwareBox.SetLabelText(Constants.HARDWARE_PANEL_NAME)
        self.hardwareBox.SetForegroundColour(wx.WHITE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.controlBox, 1, wx.EXPAND)
        sizer.Add(self.hardwareBox, 3, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Layout()
