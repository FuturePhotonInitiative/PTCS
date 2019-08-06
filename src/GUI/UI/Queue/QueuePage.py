from QueuePanel import QueuePanel
from ExperimentControlPanel import ExperimentControlPanel

from src.GUI.UI.Page import Page
from src.GUI.Util import CONSTANTS


class QueuePage(Page):
    """
    A page for setting up, and running a queue of experiments
    """

    def __init__(self, parent, experiments_manager, ui_controller, queue_manager):
        """
        Sets up the Queue Page
        The page has two halves
        The first half is the Experiment Control Panel, which allows viewing and adjustment of experiment variables
        The second half is the Queue Panel which displays the Queue of experiments, and allows selection
        :param parent: The wxframe that the Queue Page will be shown on
        """
        Page.__init__(self, parent)
        self.experiments_manager = experiments_manager
        self.ui_controller = ui_controller
        self.queue_manager = queue_manager

        # Sets up the sub-panels
        self.queue_panel = QueuePanel(self, queue_manager)
        self.control_panel = ExperimentControlPanel(self)
        Page.add_panels(self, self.queue_panel, self.control_panel,
                        display_propotion=CONSTANTS.QUEUE_PANEL_PROPORTION,
                        control_proportion=CONSTANTS.QUEUE_CONTROL_PANEL_PROPORTION)
