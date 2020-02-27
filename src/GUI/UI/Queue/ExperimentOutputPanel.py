import wx

import src.GUI.Util.Globals as Globals
from src.GUI.UI.ControlPanel import ControlPanel
from src.GUI.Util import CONSTANTS


class ExperimentOutputPanel(ControlPanel):
    """
    A panel for viewing and modifying the variables in an experiment
    """

    def __init__(self, parent):
        """
        Sets up an experiment control panel
        :param parent: The parent to display the panel on
        :param experiment: The experiment to use when rendering
        """
        ControlPanel.__init__(self, parent)

        self.UI_control = Globals.systemConfigManager.get_ui_controller()

        # Sets up the colors display Constants are in Util.CONSTANTS
        self.SetBackgroundColour(CONSTANTS.CONTROL_PANEL_COLOR)
        self.SetForegroundColour(CONSTANTS.CONTROL_PANEL_FOREGROUND_COLOR)

        # Sets up the vertical sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        self.out_text_field = wx.TextCtrl(self, style=style)
        self.stop_button = wx.Button(self)
        self.stop_button.SetLabelText("Back to Test List")

        self.sizer.Add(self.out_text_field, 5, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.stop_button, 1, wx.EXPAND | wx.ALL)

        self.out_text_field.SetBackgroundColour(CONSTANTS.LIST_PANEL_COLOR)
        self.out_text_field.SetForegroundColour(CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        # Renders the panel with the given experiment
        self.Bind(wx.EVT_BUTTON, self.change_mode)

    def render(self, obj):
        """
        Sets up the panel with an experiment and it's components
        :param experiment: The experiment to render the page with
        """
        pass

    def output_to_text_field(self, ui_control):
        ui_control.redirectSTDout(self.out_text_field)

    def change_mode(self, evt):
        ui_control = Globals.systemConfigManager.get_ui_controller()
        if ui_control is not None:
            ui_control.redirectSTDout(None)
            ui_control.switch_queue_to_edit()
