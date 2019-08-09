import os
import wx
from src.GUI.Util import CONSTANTS


class ResultsFileListPanel(wx.StaticBox):
    def __init__(self, parent):
        """
        Sets up the Results File List Panel
        :param parent: The parent to display the panel on
        """
        wx.StaticBox.__init__(self, parent)

        self.result = None

        self.list_box = wx.ListBox(self, style=wx.LB_HSCROLL)
        self.list_box.SetBackgroundColour(CONSTANTS.LIST_PANEL_COLOR)
        self.list_box.SetForegroundColour(CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.sizer.Add(self.list_box, 1, wx.EXPAND | wx.ALL)

        # Runs the file selection handler when a file is selected
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_result_select)

        self.render(None)

    def set_up_ui_control(self, ui_control):
        pass

    def render(self, result):
        """
        Renders the panel with an experiment, adds all of the experiments results files to the display
        :param result: The experiment who's results will be displayed
        """
        self.list_box.Clear()
        self.result = result
        if self.result is not None:
            for fil in self.result.get_experiment_results_file_list():
                self.list_box.Append(fil)

    def on_result_select(self, event):
        """
        Opens the file selected using the operating system, then deselects the selection
        :param event: The event that caused the call
        """
        file_name = self.result.get_experiment_results_file_list()[self.list_box.GetSelection()]
        os.startfile("\"{}\"".format(file_name))
        self.list_box.Deselect(self.list_box.GetSelection())
