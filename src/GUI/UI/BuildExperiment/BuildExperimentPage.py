import wx
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS
from src.GUI.UI.SpaeControlPanel import SpaeControlPanel
from src.GUI.UI.SpaeDisplayPanel import SpaeDisplayPanel
from src.GUI.UI.SpaePage import SpaePage


class BuildExperimentsPage(SpaePage):
    """

    """

    def __init__(self, parent):
        """
        Sets up the Build Experiment Page
        The page has two sections
        The first section is the scripts panel, which will display the lego like pieces for making an experiment
        The second section is the experiment panel,
            which will hold a field for building an experiment by linking lego like scripts together
        :param parent: The wxframe that the Build Experiment Page will be shown on
        """
        SpaePage.__init__(self, parent)

        # Sets up the sub-panels
        self.experiments_panel = SpaeDisplayPanel(self)
        self.scripts_panel = SpaeControlPanel(self)
        SpaePage.add_panels(self, self.experiments_panel, self.scripts_panel,
                        display_propotion=CONSTANTS.BUILD_PANEL_PROPORTION,
                        control_proportion=CONSTANTS.BUILD_SCRIPT_PANEL_PROPORTION)