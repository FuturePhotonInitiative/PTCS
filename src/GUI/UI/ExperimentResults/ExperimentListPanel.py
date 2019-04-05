import wx
from src.GUI.Util import GUI_CONSTANTS
import src.GUI.Util.Globals as Globals


class ExperimentListPanel(wx.StaticBox):
    """
    Panel for displaying a list of the experiments that have been run
    """

    def __init__(self, parent):
        """
        Sets up the experiment list panel
        :param parent: The parent to display the panel on
        """
        wx.StaticBox.__init__(self, parent)
        self.root = None


        self.list_box = wx.TreeCtrl(self)
        # self.list_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.list_box_sizer.Add(self.list_box, 5)

        # Sets up the colors display Constants are in Util.CONSTANTS
        self.list_box.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.list_box.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        # Adds all the experiments in the application queue to the display list

        self.root = None
        self.reload_panel(None)

        self.run_button = wx.Button(self)
        self.run_button.SetLabelText("Reload the Results")


        # Runs deselect_and_return_control_to_default on a double click or when escape is pressed
        self.Bind(wx.EVT_KEY_DOWN, self.deselect_and_return_control_to_default)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.deselect_and_return_control_to_default)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.sizer.Add(self.list_box, 5, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.run_button, 1, wx.EXPAND | wx.ALL)

        # Runs the on_experiment_select function when an experiment is selected
        self.Bind(wx.EVT_LISTBOX, self.on_experiment_select)
        self.Bind(wx.EVT_BUTTON, self.reload_panel)


    def deselect_and_return_control_to_default(self, event):
        """
        Deselects the selected experiment, and tells the parent to render the default results file list panel
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

    def reload_panel(self, event):
        """
        Reloads it self, updates if the Queue has changed
        """
        if not self.root:
            self.root = self.list_box.AddRoot(GUI_CONSTANTS.EXPERIMENT_QUEUE_RESULT_ROOT)
        self.list_box.DeleteChildren(self.root)
        for que_result in Globals.systemConfigManager.get_results_manager().get_queue_results():
            que_root = self.list_box.AppendItem(self.root, que_result.get_name())
            for exp_result_name in que_result.get_experiment_results_list():
                self.list_box.AppendItem(que_root, exp_result_name)
        self.list_box.ExpandAll()