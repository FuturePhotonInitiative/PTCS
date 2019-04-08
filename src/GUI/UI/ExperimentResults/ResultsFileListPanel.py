import os

import wx
from src.GUI.Util import GUI_CONSTANTS
import src.GUI.Util.Globals as Globals


class ResultsFileListPanel(wx.StaticBox):
    def __init__(self, parent):
        """
        Sets up the Results File List Panel
        :param parent: The parent to display the panel on
        """
        wx.StaticBox.__init__(self, parent)

        self.result = None

        self.list_box = wx.ListBox(self)
        self.list_box.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.list_box.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)


        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.sizer.Add(self.list_box, 1, wx.EXPAND | wx.ALL)

        # Runs the file selection handler when a file is selected
        self.Bind(wx.EVT_LISTBOX, self.on_result_select)

        self.render_panel(None)

    def on_result_select(self, event):
        """
        Opens the file selected using the operating system, then deselects the selection
        :param event: The event that caused the call
        """

        # Todo open the file selected
        os.system("start "+self.result.get_experiment_results_file_list()[self.list_box.GetSelection()])
        self.list_box.Deselect(self.list_box.GetSelection())

    def render_panel(self, result):
        """
        Renders the panel with an experiment, adds all of the experiments results files to the display
        :param result: The experiment who's results will be displayed
        """
        self.list_box.Clear()
        self.result = result
        if self.result is not None:
            for file in self.result.get_experiment_results_file_list():
                self.list_box.Append(file)
