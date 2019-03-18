import wx
from ExperimentListPanel import ExperimentListPanel
from ResultsFileListPanel import ResultsFileListPanel
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS


class ExperimentResultsPage(wx.Panel):
    """
    A page for displaying the experiments that have been run
    and the files that they created as results
    """

    def __init__(self, parent):
        """
        Sets up the Experiment Results Page
        The page has two halves
        The first half is the ExperimentListPanel which lists all experiments that have been run in their Queues
        The second half is the ResultsFileListPanel which shows all the files for the selected experiment or Queue
        :param parent: The wxframe that the Experiment Results Page will be shown on
        """
        wx.Panel.__init__(self, parent)

        # Sets up both the halves of the page
        self.experiment_list_panel = ExperimentListPanel(self)
        self.results_file_list_panel = ResultsFileListPanel(self)

        # Sets up the displays so both halves are displayed properly
        # Display constants are in Util.CONSTANTS
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.experiment_list_panel, CONSTANTS.RESULTS_EXPERIMENT_PANEL_PROPORTION, wx.EXPAND)
        sizer.Add(self.results_file_list_panel, CONSTANTS.RESULTS_FILE_PANEL_PROPORTION, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Layout()
