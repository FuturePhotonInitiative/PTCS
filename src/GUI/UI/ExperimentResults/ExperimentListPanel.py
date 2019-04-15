import wx
from src.GUI.UI.SpaeDisplayPanel import SpaeDisplayPanel
from src.GUI.Util import GUI_CONSTANTS
import src.GUI.Util.Globals as Globals


class ExperimentListPanel(SpaeDisplayPanel):
    """
    Panel for displaying a list of the experiments that have been run
    """

    def __init__(self, parent):
        """
        Sets up the experiment list panel
        :param parent: The parent to display the panel on
        """
        SpaeDisplayPanel.__init__(self, parent)
        self.root = None

        self.tree_box = wx.TreeCtrl(self)
        # self.list_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.list_box_sizer.Add(self.list_box, 5)

        # Sets up the colors display Constants are in Util.CONSTANTS
        self.tree_box.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.tree_box.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        # Adds all the experiments in the application queue to the display list

        self.root = None
        self.reload(None)

        self.run_button = wx.Button(self)
        self.run_button.SetLabelText("Reload the Results")


        # Runs deselected on a double click or when escape is pressed
        self.Bind(wx.EVT_KEY_DOWN, self.deselected)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.deselected)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.sizer.Add(self.tree_box, 5, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.run_button, 1, wx.EXPAND | wx.ALL)

        # Runs the selected function when an experiment is selected
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.selected)
        self.Bind(wx.EVT_BUTTON, self.reload)

    def set_up_ui_control(self, ui_control):
        ui_control.add_control_to_text_list(self.run_button)

    def reload(self, event=None):
        """
        Reloads it self, updates if the Queue has changed
        """
        if not self.root:
            self.root = self.tree_box.AddRoot(GUI_CONSTANTS.EXPERIMENT_QUEUE_RESULT_ROOT)
        self.tree_box.DeleteChildren(self.root)
        for que_result in Globals.systemConfigManager.get_results_manager().get_queue_results():
            que_root = self.tree_box.AppendItem(self.root, que_result.get_name())
            for exp_result_name in que_result.get_experiment_results_list():
                self.tree_box.AppendItem(que_root, exp_result_name)
        self.tree_box.ExpandAll()

    def deselected(self, event):
        """
        Deselects the selected experiment, and tells the parent to render the default results file list panel
        :param event: The event that cause the call
        """

        if (not isinstance(event, wx.KeyEvent)) or event.GetKeyCode() == wx.WXK_ESCAPE:
            selected = self.tree_box.GetItemText(self.tree_box.GetSelection())
            self.tree_box.SelectItem(selected, select=False)
            self.Parent.render_control_panel(None)

        # Todo add call to parent to render the default results file list page

    def selected(self, event):
        """
        Tells the parent to render the results page with the selected experiment
        :param event: The event that caused the call
        """
        selected = self.tree_box.GetItemText(self.tree_box.GetSelection())
        try:
            experiment_result = Globals.systemConfigManager.get_results_manager().get_experiment_result(selected)
        except KeyError:
            experiment_result = None
        self.Parent.render_control_panel(experiment_result)

