import wx
from src.GUI.Util import GUI_CONSTANTS
import src.GUI.Util.Globals as Globals


class QueuePanel(wx.ListBox):
    """
    Panel for rendering a queue of experiments
    """
    def __init__(self, parent):
        """
        Sets up the Queue Panel
        :param parent: The parent to display the panel on
        """
        wx.ListBox.__init__(self, parent)

        # Sets up the colors display Constants are in Util.CONSTANTS
        self.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        # Adds all the experiments in the application queue to the display list
        for experiment in Globals.ExperimentQueue.get_experiment_names():
            self.Append(experiment)

        # Runs deselect_and_return_control_to_default on a double click or when escape is pressed
        self.Bind(wx.EVT_KEY_DOWN, self.deselect_and_return_control_to_default)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.deselect_and_return_control_to_default)

        # Runs the on_experiment_select function when an experiment is selected
        self.Bind(wx.EVT_LISTBOX, self.on_experiment_select)

    def deselect_and_return_control_to_default(self, event):
        """
        Deselects the selected experiment, and tells the parent to render the default control panel
        :param event: The event that cause the call
        """
        self.GetParent().render_control_panel_with_experiment(None)
        if (not isinstance(event, wx.KeyEvent)) or event.GetKeyCode() == wx.WXK_ESCAPE:
            for selected in self.GetSelections():
                self.Deselect(selected)

    def on_experiment_select(self, event):
        """
        Tells the parent to render the control panel with the selected experiment
        :param event: The event that caused the call
        """
        selected_experiment = Globals.systemConfigManager.get_experiments_manager()
        self.GetParent().render_control_panel_with_experiment(selected_experiment)
        pass

    def reload_panel(self):
        """
        Reloads the display list with the current Queue contents
        """
        self.Clear()
        for experiment in Globals.ExperimentQueue.get_experiment_names():
            self.Append(experiment)
