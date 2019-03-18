import wx
from src.GUI.Util import GUI_CONSTANTS
from HardwareListPanel import HardwareListPanel

import src.GUI.Util.GUI_CONSTANTS as CONSTANTS


class HardwarePage(wx.Panel):
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
        wx.Panel.__init__(self, parent)

        # Sets up the sub-panels
        self.hardwareConfigurationListPanel = HardwareListPanel(self)
        self.controlPanel = wx.StaticBox(self)

        # Setting up display for the Hardware list panel
        # Display constants can be found in Util.CONSTANTS
        self.hardwareConfigurationListPanel.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.hardwareConfigurationListPanel.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        # Adds the sub-panels to the page and sizes them appropriately, adds labels if necessary
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_side = wx.BoxSizer(wx.VERTICAL)
        right_side.Add(wx.StaticText(self, label=CONSTANTS.HARDWARE_PANEL_NAME), CONSTANTS.QUEUE_LABEL_PROPORTION, wx.TOP)
        right_side.Add(self.hardwareConfigurationListPanel, 1, wx.EXPAND | wx.ALL)
        sizer.Add(self.controlPanel, CONSTANTS.HARDWARE_CONTROL_PANEL_PROPORTION, wx.EXPAND, CONSTANTS.LIST_PANEL_MARGIN)
        sizer.Add(right_side, CONSTANTS.HARDWARE_PANEL_PROPORTION, wx.EXPAND, CONSTANTS.LIST_PANEL_MARGIN)

        self.SetSizer(sizer)
        sizer.Layout()
