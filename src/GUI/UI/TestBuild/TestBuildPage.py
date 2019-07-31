from src.GUI.UI.TestBuild.TestBuildPanel import TestBuildPanel
from src.GUI.UI.TestBuild.TestButtonPanel import TestButtonPanel
from src.GUI.UI.Page import Page
from src.GUI.Util import CONSTANTS


class TestBuildPage(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.build_panel = TestBuildPanel(self)
        self.button_panel = TestButtonPanel(self)

        Page.add_panels(self, self.build_panel, self.button_panel,
                        display_propotion=CONSTANTS.TEST_BUTTON_PANEL_PROPORTION,
                        control_proportion=CONSTANTS.TEST_BUILD_PANEL_PROPORTION)
