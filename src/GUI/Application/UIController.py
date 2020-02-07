import sys
import wx

from src.GUI.UI.Queue.ExperimentControlPanel import ExperimentControlPanel
from src.GUI.UI.Queue.ExperimentOutputPanel import ExperimentOutputPanel


class UIController:
    def __init__(self, mainframe):
        assert (mainframe is not None)
        self.mainframe = mainframe
        self.controls_to_fix_text_size = []
        self.mainframe.queue_page.set_up_ui_control(self)
        self.mainframe.hardware_page.set_up_ui_control(self)
        # self.mainframe.build_experiments_page.set_up_ui_control(self)
        self.mainframe.experiment_results_page.set_up_ui_control(self)

    def rebuild_queue_page(self):
        self.mainframe.queue_page.reload_display_panel()

    def add_control_to_text_list(self, control):
        if control is not None:
            self.controls_to_fix_text_size.append(control)
            self.fix_control_list()

    def remove_control_from_text_list(self, control):
        if control is not None and control in self.controls_to_fix_text_size:
            self.controls_to_fix_text_size.remove(control)

    def fix_control_list(self):
        for control in self.controls_to_fix_text_size:
            # print control
            UIController.fix_text_size(control, 10)

    def switch_to_result(self):
        # self.mainframe.notebook
        pass

    def redirectSTDout(self, logger):
        if logger:
            sys.stdout = logger
        else:
            sys.stdout = sys.__stdout__

    def test_added_to_config_directory(self):
        """
        When a test is built using the GUI, it puts a config file in the configs directory. This method tells the
        experiments drop-down to refresh itself
        """
        self.mainframe.queue_page.control_panel.render_without_experiment()

    def switch_queue_to_running(self):
        self.mainframe.queue_page.set_control(ExperimentOutputPanel(self.mainframe.queue_page))
        self.mainframe.queue_page.control_panel.set_up_ui_control(self)

    def switch_queue_to_edit(self):
        self.mainframe.queue_page.set_control(ExperimentControlPanel(self.mainframe.queue_page))
        self.mainframe.queue_page.control_panel.set_up_ui_control(self)

    @staticmethod
    def fix_text_size(control, margin):
        try:
            font = control.GetFont()
            # print font
            # size = wx.Size(control.GetSize().Get()[1] / 4, control.GetSize().Get()[1] / 4)
            # print size
            wx.Font.Scale(font, round((float(control.GetSize().Get()[1] - margin) /
                                       float(font.GetPixelSize()[1])) / 2.0))
            # wx.Font.SetPixelSize(font, size)
            dc = wx.ScreenDC()
            dc.SetFont(font)
            w, h = dc.GetTextExtent("test string")
            if w + margin > control.GetSize().Get()[0] and \
                    control.GetSize().Get()[0] * (float(control.GetSize().Get()[0] - margin) / float(w)) > 0:
                # print 2
                scale = round(float(control.GetSize().Get()[0] - margin) / float(w), 2)
                wx.Font.Scale(font, scale)
                # print scale
            control.SetFont(font)
        except Exception as e:
            pass
