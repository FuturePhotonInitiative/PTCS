import wx
from src.GUI.Util import CONSTANTS


class Page(wx.Panel):
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

        self.display_title = display_title
        self.control_title = control_title

        self.display_propotion = display_propotion
        self.control_proportion = control_proportion

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.right_side = wx.BoxSizer(wx.VERTICAL)
        self.left_side = wx.BoxSizer(wx.VERTICAL)

        # sets up right sub-panel
        if self.display_title is not None:
            self.right_side.Add(wx.StaticText(self, label=self.display_title), CONSTANTS.LABEL_PROPORTION, wx.TOP)
        self.right_side.Add(self.display_panel, 1, wx.EXPAND | wx.ALL)

        # sets up left sub-panel
        if self.control_title is not None:
            self.left_side.Add(wx.StaticText(self, label=self.control_title), CONSTANTS.LABEL_PROPORTION, wx.TOP)
        self.left_side.Add(self.control_panel, 1, wx.EXPAND | wx.ALL)

        sizer.Add(self.right_side, self.display_propotion, wx.EXPAND | wx.ALL)
        sizer.Add(self.left_side, self.control_proportion, wx.EXPAND | wx.ALL)

        self.SetSizer(sizer)
        sizer.Layout()

    def render_control_panel(self, model_object):
        self.control_panel.render(model_object)

    def reload_display_panel(self):
        self.display_panel.reload()

    def set_up_ui_control(self, ui_control):
        self.display_panel.set_up_ui_control(ui_control)
        self.control_panel.set_up_ui_control(ui_control)

    def set_display(self,
                   display_panel,
                   display_title=None,
                   display_propotion=1):
        self.display_panel = display_panel

        if display_title:
            self.display_title = display_title

        if display_propotion != 1:
            self.display_propotion = display_propotion

        self.right_side.Clear(delete_windows=True)
        if self.display_title is not None:
            self.right_side.Add(wx.StaticText(self, label=self.display_title), CONSTANTS.LABEL_PROPORTION, wx.TOP)
        self.right_side.Add(self.display_panel, 1, wx.EXPAND | wx.ALL)

        self.GetSizer().Layout()

    def set_control(self,
                    control_panel,
                    control_title=None,
                    control_proportion=1):
        self.control_panel = control_panel

        if control_title:
            self.control_title = control_title

        if control_proportion != 1:
            self.control_proportion = control_proportion

        self.left_side.Clear(delete_windows=True)
        if self.control_title is not None:
            self.left_side.Add(wx.StaticText(self, label=self.control_title), CONSTANTS.LABEL_PROPORTION, wx.TOP)
        self.left_side.Add(self.control_panel, 1, wx.EXPAND | wx.ALL)

        self.GetSizer().Layout()
