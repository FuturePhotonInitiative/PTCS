import wx

QUEUE_PANEL_NAME = "Experiments"
QUEUE_PANEL_COLOR = wx.BLACK#wx.Colour(100, 100, 100)


class QueuePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.queueBox = QueuePanel(self)
        self.controlBox = wx.StaticBox(self)

        # self.queueBox.SetForegroundColour(wx.WHITE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.controlBox, 1, wx.EXPAND | wx.ALL)
        sizer.Add(self.queueBox, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Layout()


class QueuePanel(wx.ListBox):
    def __init__(self, parent):
        wx.ListBox.__init__(self, parent)

        self.SetBackgroundColour(QUEUE_PANEL_COLOR)
        self.SetForegroundColour(wx.GREEN)
        # self.AppendColumn(QUEUE_PANEL_NAME)
        self.Append("Test 1")
        self.Append("Test 2")
        self.Append("Test 3")
        self.Append("Test 4")
        self.Append("Test 5")
        self.Append("Test 6")

        self.Bind(wx.EVT_KEY_DOWN, self.returnToMainControl)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.returnToMainControl)

    def returnToMainControl(self, event):
        if (not isinstance(event, wx.KeyEvent)) or event.GetKeyCode() == wx.WXK_ESCAPE:
            for selected in self.GetSelections():
                self.Deselect(selected)
