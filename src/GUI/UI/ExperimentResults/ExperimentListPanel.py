import wx
from src.GUI.UI.DisplayPanel import DisplayPanel
from src.GUI.Util import CONSTANTS
import src.GUI.Util.Globals as Globals


class ExperimentListPanel(DisplayPanel):
    """
    Panel for displaying a list of the experiments that have been run
    """

    def __init__(self, parent):
        """
        Sets up the experiment list panel
        :param parent: The parent to display the panel on
        """
        DisplayPanel.__init__(self, parent)
        self.root = None

        self.tree_box = wx.TreeCtrl(self)
        # self.list_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.list_box_sizer.Add(self.list_box, 5)

        # Sets up the colors display Constants are in Util.CONSTANTS
        self.tree_box.SetBackgroundColour(CONSTANTS.LIST_PANEL_COLOR)
        self.tree_box.SetForegroundColour(CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        # Adds all the experiments in the application queue to the display list

        self.root = None

        # self.run_button = wx.Button(self)
        # self.run_button.SetLabelText("Reload the Results")


        # Runs deselected on a double click or when escape is pressed
        self.Bind(wx.EVT_KEY_DOWN, self.deselected)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.deselected)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.sizer.Add(self.tree_box, 5, wx.EXPAND | wx.ALL)
        # self.sizer.Add(self.run_button, 1, wx.EXPAND | wx.ALL)

        # Runs the selected function when an experiment is selected
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.selected)
        # self.Bind(wx.EVT_BUTTON, self.reload)
        # self.Bind(wx.EVT_TIMER, self.reload, self.Parent.Parent.Parent.Parent.timer)

        # self.timer = wx.Timer(self)
        # self.Bind(wx.EVT_TIMER, self.reload, self.timer)
        # self.timer.Start(5000)

        self.load_queues()

    def set_up_ui_control(self, ui_control):
        pass

    def add_queue_to_view(self, queue_result):
        """
        Adds a queue to the UI
        :param queue_result: the queue result object
        :return: the TreeRoot UI object created
        """
        result_root = self.tree_box.AppendItem(self.root, queue_result.get_name())
        for exp_result_name in queue_result.get_experiment_results_list():
            self.tree_box.AppendItem(result_root, exp_result_name)
        return result_root

    def load_queues(self):
        """
        Populate the UI based on the queue results retrieved from the filesystem when the application started
        """
        self.root = self.tree_box.AddRoot(CONSTANTS.EXPERIMENT_QUEUE_RESULT_ROOT)
        for que_result in Globals.systemConfigManager.get_results_manager().get_queue_results():
            self.add_queue_to_view(que_result)
        self.tree_box.ExpandAll()

    def append_just_run_queue(self):
        """
        Will be called when a queue has just been finished running
        Expands the control to make it visible to a user who does not know how to use tree views
        """
        queue_result = Globals.systemConfigManager.get_results_manager().get_queue_results()[-1]
        result_root = self.add_queue_to_view(queue_result)
        self.tree_box.Expand(result_root)

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

