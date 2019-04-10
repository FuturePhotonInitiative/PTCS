import wx
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS


class SpaePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.display_panel = None
        self.control_panel = None

    def add_panels(self,
                   display_panel, control_panel,
                   display_title=None, control_title=None,
                   display_propotion=1, control_proportion=1):
        self.display_panel = display_panel
        self.control_panel = control_panel

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # sets up right sub-panel
        right_side = wx.BoxSizer(wx.VERTICAL)
        if display_title is not None:
            right_side.Add(wx.StaticText(self, label=display_title), CONSTANTS.LABEL_PROPORTION, wx.TOP)
        right_side.Add(self.display_panel, 1, wx.EXPAND | wx.ALL)

        # sets up left sub-panel
        left_side = wx.BoxSizer(wx.VERTICAL)
        if control_title is not None:
            left_side.Add(wx.StaticText(self, label=control_title), CONSTANTS.LABEL_PROPORTION, wx.TOP)
        left_side.Add(self.control_panel, 1, wx.EXPAND | wx.ALL)

        sizer.Add(right_side, display_propotion, wx.EXPAND | wx.ALL)
        sizer.Add(self.control_panel, control_proportion, wx.EXPAND | wx.ALL)

        self.SetSizer(sizer)
        sizer.Layout()

    def render_control_panel(self, model_object):
        self.control_panel.render(model_object)

    def reload_display_panel(self):
        self.display_panel.reload()

    def set_up_ui_control(self):
        self.display_panel.set_up_ui_control()
        self.control_panel.set_up_ui_control()
