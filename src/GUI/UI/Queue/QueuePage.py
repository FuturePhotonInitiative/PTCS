import os
import wx
from src.GUI.UI.Queue.QueuePanel import QueuePanel
from src.GUI.UI.Queue.ExperimentControlPanel import ExperimentControlPanel
import src.GUI.Util.Globals as Globals

class QueuePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.queueBox = QueuePanel(self)
        self.controlBox = ExperimentControlPanel(self, None)

        # self.queueBox.SetForegroundColour(wx.WHITE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.controlBox, 1, wx.EXPAND | wx.ALL)
        sizer.Add(self.queueBox, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Layout()

    # TODO Add method to render the controlBox with the correct experiment that the QueuePanel can call
    def render_control_box_with_experiment(self, experiment):
        self.controlBox.render_with_experiment(experiment)

    def get_experiments(self):
        # print os.listdir(CONSTANTS.CONFIG_PATH)
        print type(os.listdir(Globals.ExperimentQueue.get_default_experiment_root()))
        return os.listdir(Globals.ExperimentQueue.get_default_experiment_root())

    def reload(self):
        self.queueBox.reload_panel()