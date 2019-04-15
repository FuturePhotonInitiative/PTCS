from src.GUI.UI.SpaeControlPanel import SpaeControlPanel
from src.GUI.UI.SpaePage import SpaePage
from HardwareListPanel import HardwareListPanel
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS



class HardwarePage(SpaePage):
    """
    A page for displaying and modifying hardware configurations
    """

    def __init__(self, parent):
        """
        Sets up the Hardware Page
        The page has two halves
        The first half is the Controls panel, it allows viewing and editing the settings of a hardware configuration
        The second half is the Hardware listing page which lists the existing hardware configurations
        :param parent: The wxframe that the Hardware Page will be shown on
        """

        # Attaching self to the parent
        SpaePage.__init__(self, parent)

        # Sets up the sub-panels
        self.hardwareConfigurationListPanel = HardwareListPanel(self)
        self.control_panel = SpaeControlPanel(self)
        self.add_panels(self.hardwareConfigurationListPanel, self.control_panel,
                        display_propotion=CONSTANTS.HARDWARE_PANEL_PROPORTION,
                        control_proportion=CONSTANTS.HARDWARE_CONTROL_PANEL_PROPORTION)
