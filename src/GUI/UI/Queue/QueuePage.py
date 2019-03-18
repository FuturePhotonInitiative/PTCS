import os
import wx
from src.GUI.UI.Queue.QueuePanel import QueuePanel
from src.GUI.UI.Queue.ExperimentControlPanel import ExperimentControlPanel
import src.GUI.Util.Globals as Globals
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS


class QueuePage(wx.Panel):
    """
    A page for setting up, and running a queue of experiments
    """

    def __init__(self, parent):
        """
        Sets up the Queue Page
        The page has two halves
        The first half is the Experiment Control Panel, which allows viewing and adjustment of experiment variables
        The second half is the Queue Panel which displays the Queue of experiments, and allows selection
        :param parent: The wxframe that the Queue Page will be shown on
        """
        wx.Panel.__init__(self, parent)

        # sets up both sub-panels
        self.queue_panel = QueuePanel(self)
        self.control_panel = ExperimentControlPanel(self, None)

        # Adds the sub-panels to the page and sizes them appropriately, adds labels if necessary
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_side = wx.BoxSizer(wx.VERTICAL)
        right_side.Add(wx.StaticText(self, label=CONSTANTS.QUEUE_PANEL_NAME), CONSTANTS.QUEUE_LABEL_PROPORTION, wx.TOP)
        right_side.Add(self.queue_panel, 1, wx.EXPAND | wx.ALL)
        sizer.Add(self.control_panel, CONSTANTS.QUEUE_CONTROL_PANEL_PROPORTION, wx.EXPAND | wx.ALL)
        sizer.Add(right_side, CONSTANTS.QUEUE_PANEL_PROPORTION, wx.EXPAND | wx.ALL, CONSTANTS.LIST_PANEL_MARGIN)

        self.SetSizer(sizer)
        sizer.Layout()

    def render_control_panel_with_experiment(self, experiment):
        """
        Passes an experiment to the control panel and has it rerender
        :param experiment: The experiment for the control panel to render with
        """
        self.control_panel.render_with_experiment(experiment)

    def get_experiment_classes(self):
        """
        Gets all the names of experiments classes for selection when adding a new experiment to the queue
        :return: A list of available experiments names
        """
        return os.listdir(Globals.ExperimentQueue.get_default_experiment_root())

    def reload(self):
        """
        Reloads the Queue panel to display any changes
        """
        self.queue_panel.reload_panel()
