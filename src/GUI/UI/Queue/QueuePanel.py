import wx
from src.GUI.Util import GUI_CONSTANTS


class QueuePanel(wx.ListBox):
    def __init__(self, parent):
        wx.ListBox.__init__(self, parent)

        self.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)
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
