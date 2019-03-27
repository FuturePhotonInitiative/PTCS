import wx
from src.GUI.Util import GUI_CONSTANTS
import src.GUI.Util.Globals as Globals


class HardwareListPanel(wx.ListBox):
    """
    Panel for displaying a list of hardware configs
    """

    def __init__(self, parent):
        """
        Sets up the Hardware List Panel
        :param parent: The parent to display the panel on
        """
        wx.ListBox.__init__(self, parent)

        # Setting up display for the Hardware list panel
        # Display constants can be found in Util.CONSTANTS
        self.SetBackgroundColour(GUI_CONSTANTS.LIST_PANEL_COLOR)
        self.SetForegroundColour(GUI_CONSTANTS.LIST_PANEL_FOREGROUND_COLOR)

        # Adds all the hardware to the display
        for hardware in Globals.systemConfigManager.get_hardware_manager().get_all_hardware_names():
            self.Append(hardware)

        # Runs the deselect and default function when hardware is deselected
        self.Bind(wx.EVT_KEY_DOWN, self.deselect_and_return_control_to_default)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.deselect_and_return_control_to_default)

        # Renders the selected hardware config
        self.Bind(wx.EVT_LISTBOX, self.on_hardware_select)

    def deselect_and_return_control_to_default(self, event):
        """
        Deselects the selected hardware config, and tells the parent to render the default config control panel
        :param event: The event that cause the call
        """
        if (not isinstance(event, wx.KeyEvent)) or event.GetKeyCode() == wx.WXK_ESCAPE:
            for selected in self.GetSelections():
                self.Deselect(selected)

    def on_hardware_select(self, event):
        """
        Renders a selected hardware config
        :param event: The event that triggered the call
        """
        # Todo add call to render in parent
        pass

    def reload_panel(self):
        """
        Reloads the list of hardware names
        :return:
        """
        self.Clear()
        for hardware in Globals.Hardware.get_hardware_names():
            self.Append(hardware)