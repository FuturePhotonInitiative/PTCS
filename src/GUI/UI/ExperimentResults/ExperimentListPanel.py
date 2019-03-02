import wx
from src.GUI.Util import GUI_CONSTANTS
import src.GUI.Util.Globals as Globals


class ExperimentListPanel(wx.ListBox):
    def __init__(self, parent):
        wx.ListBox.__init__(self, parent)

        self.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)
        # self.AppendColumn(QUEUE_PANEL_NAME)
        for experiment in Globals.ExperimentQueue.get_experiment_names():
            self.Append(experiment)

        self.Bind(wx.EVT_KEY_DOWN, self.return_to_main_control)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.return_to_main_control)
        self.Bind(wx.EVT_LISTBOX, self.on_hardware_select)

    def return_to_main_control(self, event):
        # self.GetParent().render_control_box_with_experiment(None)
        if (not isinstance(event, wx.KeyEvent)) or event.GetKeyCode() == wx.WXK_ESCAPE:
            for selected in self.GetSelections():
                self.Deselect(selected)

    def on_hardware_select(self, event):
        # selected_experiment = Globals.ExperimentQueue.get_ith_experiment(self.GetSelection())
        # self.GetParent().render_control_box_with_experiment(selected_experiment)
        pass

    def reload_panel(self):
        self.Clear()
        for experiment in Globals.ExperimentQueue.get_experiment_names():
            self.Append(experiment)