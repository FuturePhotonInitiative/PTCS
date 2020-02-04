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
        self.displayed_files = []

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
        self.displayed_files.clear()
        self.result = result
        if self.result is not None:
            self.list_box.Append(self.result.get_results_dir())
            self.displayed_files.append(self.result.get_results_dir())
            leng = len(self.result.get_results_dir()) + 1

            for root, dirs, files in os.walk(self.result.get_results_dir()):
                for name in files:
                    pat = os.path.join(root, name)
                    self.list_box.Append(pat[leng:])
                    self.displayed_files.append(pat)

    def on_result_select(self, event):
        """
        Opens the file selected using the operating system, then deselects the selection
        :param event: The event that caused the call
        """
        clicked_label_position = self.list_box.GetSelection()

        os.startfile("\"{}\"".format(self.displayed_files[clicked_label_position]))
        self.list_box.Deselect(self.list_box.GetSelection())
