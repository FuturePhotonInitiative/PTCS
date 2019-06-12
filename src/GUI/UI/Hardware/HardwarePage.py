from src.GUI.UI.ControlPanel import ControlPanel
from src.GUI.UI.Page import Page
from HardwareListPanel import HardwareListPanel
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS



class HardwarePage(Page):
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
        Page.__init__(self, parent)

        # Sets up the sub-panels
        self.hardwareConfigurationListPanel = HardwareListPanel(self)
        self.control_panel = ControlPanel(self)
        self.add_panels(self.hardwareConfigurationListPanel, self.control_panel,
                        display_propotion=CONSTANTS.HARDWARE_PANEL_PROPORTION,
                        control_proportion=CONSTANTS.HARDWARE_CONTROL_PANEL_PROPORTION)
