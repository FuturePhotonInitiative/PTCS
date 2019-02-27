import wx
import src.Gui.Util.GUI_CONSTANTS


class ExperimentControlPanel(wx.StaticBox):
    def __init__(self, parent, experiment):
        wx.StaticBox.__init__(self, parent)

        self.SetBackgroundColour(src.Gui.Util.GUI_CONSTANTS.CONTROL_PANEL_COLOR)
        self.SetForegroundColour(src.Gui.Util.GUI_CONSTANTS.CONTROL_PANEL_FOREGROUND_COLOR)

        self.Bind(wx.EVT_KEY_DOWN, self.returnToMainControl)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.returnToMainControl)

    def returnToMainControl(self, event):
        if (not isinstance(event, wx.KeyEvent)) or event.GetKeyCode() == wx.WXK_ESCAPE:
            for selected in self.GetSelections():
                self.Deselect(selected)
