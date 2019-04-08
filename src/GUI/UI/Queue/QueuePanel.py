import wx
from wx import Font

from src.GUI.Util import GUI_CONSTANTS
import src.GUI.Util.Globals as Globals
from src.GUI.Util.Functions import fix_text_size


class QueuePanel(wx.StaticBox):
    """
    Panel for rendering a queue of experiments
    """
    def __init__(self, parent):
        """
        Sets up the Queue Panel
        :param parent: The parent to display the panel on
        """
        wx.StaticBox.__init__(self, parent)

        self.list_box = wx.ListBox(self)
        # self.list_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.list_box_sizer.Add(self.list_box, 5)
        self.run_button = wx.Button(self)
        self.run_button.SetLabelText("Run Queue")
        # self.run_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.sizer.Add(self.list_box_sizer, 5)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.sizer.Add(self.list_box, 5, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.run_button, 1, wx.EXPAND | wx.ALL)

        # Sets up the colors display Constants are in Util.CONSTANTS
        self.list_box.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.list_box.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        # Adds all the experiments in the application queue to the display list
        self.reload_panel()

        # Runs deselect_and_return_control_to_default on a double click or when escape is pressed
        self.Bind(wx.EVT_KEY_DOWN, self.deselect_and_return_control_to_default)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.deselect_and_return_control_to_default)

        # Runs the on_result_select function when an experiment is selected
        self.Bind(wx.EVT_LISTBOX, self.on_experiment_select)


        # Runs the queue when the run button is pressed
        self.Bind(wx.EVT_BUTTON, self.run_the_queue)

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

        queue_manager = Globals.systemConfigManager.get_queue_manager()
        selected_experiment = queue_manager.get_ith_experiment(self.list_box.GetSelection())
        self.GetParent().render_control_panel_with_experiment(selected_experiment)
        pass


    def reload_panel(self):
        """
        Reloads the display list with the current Queue contents
        """
        self.list_box.Clear()
        fix_text_size(self.run_button, 10)
        for experiment in Globals.systemConfigManager.get_queue_manager().get_experiment_names():
            self.list_box.Append(experiment)

    def run_the_queue(self, event):
        Globals.systemConfigManager.get_queue_manager().run()