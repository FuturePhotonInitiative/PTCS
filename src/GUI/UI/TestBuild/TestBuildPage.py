from src.GUI.UI.TestBuild.TestBuildPanel import TestBuildPanel
from src.GUI.UI.TestBuild.TestButtonPanel import TestButtonPanel
from src.GUI.UI.Page import Page
from src.GUI.Util import CONSTANTS


class TestBuildPage(Page):
    """
    A page for building custom tests.
    """
    def __init__(self, parent, hardware_manager):
        """
        Sets up the Test Build Page
        The page has two halves
        The first half is the Test Button Panel, which contains the buttons for different test functions
        The second half is the Test Build Panel which displays the lines of the current test being built
        and allows editing the lines and saving the test.
        :param parent: The wxframe that the Test Build Page will be shown on
        """
        Page.__init__(self, parent)
        self.build_panel = TestBuildPanel(self, hardware_manager)
        self.button_panel = TestButtonPanel(self, hardware_manager)

        Page.add_panels(self, self.build_panel, self.button_panel,
                        display_propotion=CONSTANTS.TEST_BUTTON_PANEL_PROPORTION,
                        control_proportion=CONSTANTS.TEST_BUILD_PANEL_PROPORTION)
