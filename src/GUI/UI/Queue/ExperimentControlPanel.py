import wx
import src.GUI.Util.GUI_CONSTANTS


class ExperimentControlPanel(wx.StaticBox):
    def __init__(self, parent, experiment):
        wx.StaticBox.__init__(self, parent)

        self.SetBackgroundColour(src.GUI.Util.GUI_CONSTANTS.CONTROL_PANEL_COLOR)
        self.SetForegroundColour(src.GUI.Util.GUI_CONSTANTS.CONTROL_PANEL_FOREGROUND_COLOR)

        self.Bind(wx.EVT_KEY_DOWN, self.returnToMainControl)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.returnToMainControl)

    def render_without_experiment(self):
        pass

    def render_with_experiment(self, experiment):
        pass
