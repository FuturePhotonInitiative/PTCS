import wx

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

        # Sets up the colors display Constants are in Util.CONSTANTS
        self.SetBackgroundColour(CONSTANTS.CONTROL_PANEL_COLOR)
        self.SetForegroundColour(CONSTANTS.CONTROL_PANEL_FOREGROUND_COLOR)

        # Sets up the vertical sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        self.out_text_field = wx.TextCtrl(self, style=style)
        self.stop_button = wx.Button(self)
        self.stop_button.SetLabelText("Exit")

        self.sizer.Add(self.out_text_field, 5, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.stop_button, 1, wx.EXPAND | wx.ALL)

        self.out_text_field.SetBackgroundColour(CONSTANTS.LIST_PANEL_COLOR)
        self.out_text_field.SetForegroundColour(CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        # Renders the panel with the given experiment
        self.Bind(wx.EVT_BUTTON, self.change_mode)

        self.ui_controller = None

    def set_up_ui_control(self, ui_control):
        self.ui_controller = ui_control
        ui_control.redirectSTDout(self.out_text_field)

    def render(self, obj):
        """
        Sets up the panel with an experiment and it's components
        :param experiment: The experiment to render the page with
        """
        pass

    def change_mode(self, evt):
        if self.ui_controller is not None:
            self.ui_controller.redirectSTDout(None)
            self.ui_controller.switch_queue_to_edit()
