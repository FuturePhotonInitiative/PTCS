from ExperimentListPanel import ExperimentListPanel
from ResultsFileListPanel import ResultsFileListPanel
from src.GUI.UI.Page import Page
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS


class ExperimentResultsPage(Page):
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
        Page.__init__(self, parent)

        # Sets up both the halves of the page
        self.experiment_list_panel = ExperimentListPanel(self)
        self.results_file_list_panel = ResultsFileListPanel(self)

        Page.add_panels(self, self.experiment_list_panel, self.results_file_list_panel,
                        display_propotion=CONSTANTS.RESULTS_EXPERIMENT_PANEL_PROPORTION,
                        control_proportion=CONSTANTS.RESULTS_FILE_PANEL_PROPORTION)
