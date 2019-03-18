import wx
from src.GUI.Util import GUI_CONSTANTS
import src.GUI.Util.Globals as Globals


class ExperimentListPanel(wx.ListBox):
    """
    Panel for displaying a list of the experiments that have been run
    """

    def __init__(self, parent):
        """
        Sets up the experiment list panel
        :param parent: The parent to display the panel on
        """
        wx.ListBox.__init__(self, parent)

        # Sets up the colors display Constants are in Util.CONSTANTS
        self.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        # Adds all the experiments in the application queue to the display list
        for experiment in Globals.ExperimentQueue.get_experiment_names():
            self.Append(experiment)

        # Runs return_to_main_control on a double click or when escape is pressed
        self.Bind(wx.EVT_KEY_DOWN, self.return_to_main_control)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.return_to_main_control)

        # Runs the on_experiment_select function when an experiment is selected
        self.Bind(wx.EVT_LISTBOX, self.on_experiment_select)

    def return_to_main_control(self, event):
        """
        Deselects the selected experiment, and tells the parent to render the default results file list page
        :param event: The event that cause the call
        """

        if (not isinstance(event, wx.KeyEvent)) or event.GetKeyCode() == wx.WXK_ESCAPE:
            for selected in self.GetSelections():
                self.Deselect(selected)

        # Todo add call to parent to render the default results file list page

    def on_experiment_select(self, event):
        """
        Tells the parent to render the results page with the selected experiment
        :param event: The event that caused the call
        """
        # Todo add call to parent to render the results file list page with an experiment
        pass

    def reload_panel(self):
        """
        Reloads it self, updates if the Queue has changed
        """
        self.Clear()
        for experiment in Globals.ExperimentQueue.get_experiment_names():
            self.Append(experiment)