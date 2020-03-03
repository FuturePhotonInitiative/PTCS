import sys

from src.GUI.UI.Queue.ExperimentControlPanel import ExperimentControlPanel
from src.GUI.UI.Queue.ExperimentOutputPanel import ExperimentOutputPanel


class UIController:
    def __init__(self, mainframe):
        assert (mainframe is not None)
        self.mainframe = mainframe

    def rebuild_queue_page(self):
        self.mainframe.queue_page.reload_display_panel()

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
        if isinstance(self.mainframe.queue_page.control_panel, ExperimentControlPanel):
            self.mainframe.queue_page.control_panel.render_without_experiment()

    def switch_queue_to_running(self):
        control_panel = ExperimentOutputPanel(self.mainframe.queue_page)
        self.mainframe.queue_page.set_control(control_panel)
        control_panel.output_to_text_field(self)

    def switch_queue_to_edit(self):
        self.mainframe.queue_page.set_control(ExperimentControlPanel(self.mainframe.queue_page))
