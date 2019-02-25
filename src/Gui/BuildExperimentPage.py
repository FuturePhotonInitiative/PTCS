import wx


class BuildExperimentsPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.queueBox = wx.StaticBox(self)
        self.controlBox = wx.StaticBox(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.controlBox, 1, wx.EXPAND)
        sizer.Add(self.queueBox, 1, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Layout()
