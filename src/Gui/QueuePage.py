import wx


class QueuePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.queueBox = wx.StaticBox(self)
        self.controlBox = wx.StaticBox(self)
        self.queueBox.SetBackgroundColour(wx.Colour(100,100,100))
        self.queueBox.SetLabelText("Name")
        self.queueBox.SetForegroundColour(wx.WHITE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.controlBox, 1, wx.EXPAND|wx.ALL)
        sizer.Add(self.queueBox, 3, wx.EXPAND|wx.ALL)


        self.SetSizer(sizer)
        sizer.Layout()