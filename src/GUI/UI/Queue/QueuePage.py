from src.GUI.UI.Queue.QueuePanel import QueuePanel
from src.GUI.UI.Queue.ExperimentControlPanel import ExperimentControlPanel
from src.GUI.UI.SpaePage import SpaePage
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS


class QueuePage(SpaePage):
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
        SpaePage.__init__(self, parent)

        # Sets up the sub-panels
        self.queue_panel = QueuePanel(self)
        self.control_panel = ExperimentControlPanel(self)
        SpaePage.add_panels(self, self.queue_panel, self.control_panel,
                        display_propotion=CONSTANTS.QUEUE_PANEL_PROPORTION,
                        control_proportion=CONSTANTS.QUEUE_CONTROL_PANEL_PROPORTION)