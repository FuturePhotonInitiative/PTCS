import wx
from src.GUI.Util import GUI_CONSTANTS
import src.GUI.Util.Globals as Globals


class ResultsFileListPanel(wx.ListBox):
    def __init__(self, parent):
        """
        Sets up the Results File List Panel
        :param parent: The parent to display the panel on
        """
        wx.ListBox.__init__(self, parent)

        self.experiment = None

        # Runs the file selection handler when a file is selected
        self.Bind(wx.EVT_LISTBOX, self.on_file_select)

    def on_file_select(self, event):
        """
        Opens the file selected using the operating system, then deselects the selection
        :param event: The event that caused the call
        """

        # Todo open the file selected

        for selected in self.GetSelections():
                self.Deselect(selected)

    def render_panel(self, experiment):
        """
        Renders the panel with an experiment, adds all of the experiments results files to the display
        :param experiment: The experiment who's results will be displayed
        """
        self.Clear()
        self.experiment = experiment

        # Todo add all of the experiments results files to the display
