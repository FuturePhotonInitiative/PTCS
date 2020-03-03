import wx
import os

from src.GUI.UI.DisplayPanel import DisplayPanel
from src.GUI.Util.CONSTANTS import LIST_PANEL_COLOR, LIST_PANEL_FOREGROUND_COLOR, SAVED_QUEUES_DIR
import src.GUI.Util.Globals as Globals


class QueuePanel(DisplayPanel):
    """
    Panel for rendering a queue of experiments
    """
    def __init__(self, parent):
        """
        Sets up the Queue Panel
        :param parent: The tab to display the panel on
        """
        DisplayPanel.__init__(self, parent)

        self.queue_list_box = wx.ListBox(self, style=wx.LB_HSCROLL)
        self.queue_list_box.SetFont(wx.Font(wx.FontInfo(12)))

        self.run_button = wx.Button(self)
        self.run_button.SetLabelText("Run Queue")
        self.run_button.SetFont(wx.Font(wx.FontInfo(30)))
        self.run_button.Disable()

        self.clear_button = wx.Button(self)
        self.clear_button.SetLabelText("Clear Queue")
        self.clear_button.Disable()

        self.save_button = wx.Button(self)
        self.save_button.SetLabelText("Save Queue")
        self.save_button.Disable()

        self.load_button = wx.Button(self)
        self.load_button.SetLabelText("Load Queue")
        self.load_button.Disable()

        self.save_text_box = wx.TextCtrl(self)
        self.save_text_box.Disable()

        self.load_choice_box = wx.Choice(self, choices=self.get_loadable_queues())

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.sizer.Add(self.queue_list_box, 5, wx.EXPAND | wx.ALL)

        self.midbar = wx.BoxSizer(wx.HORIZONTAL)
        self.midbar.Add(self.clear_button, 1, wx.EXPAND | wx.ALL)

        self.btn_sizer = wx.BoxSizer(wx.VERTICAL)
        self.btn_sizer.Add(self.save_button, 1, wx.EXPAND | wx.ALL)
        self.btn_sizer.Add(self.load_button, 1, wx.EXPAND | wx.ALL)

        self.input_sizer = wx.BoxSizer(wx.VERTICAL)
        self.input_sizer.Add(self.save_text_box, 1, wx.EXPAND | wx.ALL)
        self.input_sizer.Add(self.load_choice_box, 1, wx.EXPAND | wx.ALL)

        self.midbar.Add(self.btn_sizer, 0.5, wx.EXPAND | wx.ALL)
        self.midbar.Add(self.input_sizer, 0.5, wx.EXPAND | wx.ALL)

        self.sizer.Add(self.midbar, 1, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.run_button, 2, wx.EXPAND | wx.ALL)

        # Sets up the colors display Constants are in Util.CONSTANTS
        self.queue_list_box.SetBackgroundColour(LIST_PANEL_COLOR)
        self.queue_list_box.SetForegroundColour(LIST_PANEL_FOREGROUND_COLOR)

        # Adds all the experiments in the application queue to the display list
        self.reload()

        self.Bind(wx.EVT_TEXT, self.check_save_button_state)
        self.load_choice_box.Bind(wx.EVT_CHOICE, self.check_load_button_state)

        # Runs deselected on a double click or when escape is pressed
        self.Bind(wx.EVT_KEY_DOWN, self.deselected)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.deselected)

        # Runs the selected function when an experiment is selected
        self.Bind(wx.EVT_LISTBOX, self.selected)

        # Runs the queue when the run button is pressed
        self.Bind(wx.EVT_BUTTON, self.run_the_queue)
        self.save_button.Bind(wx.EVT_BUTTON, self.save_queue)
        self.load_button.Bind(wx.EVT_BUTTON, self.load_queue)
        self.clear_button.Bind(wx.EVT_BUTTON, self.clear_queue)

    def reload(self):
        """
        Reloads the display list with the current Queue contents, and sets the enabled state of the save queue box
        """
        experiments = Globals.systemConfigManager.get_queue_manager().get_experiment_names()
        if len(experiments) > 0:
            self.save_button.Enable()
            self.save_text_box.Enable()
            self.run_button.Enable()
            self.clear_button.Enable()
        else:
            self.save_button.Disable()
            self.save_text_box.Disable()
            self.run_button.Disable()
            self.clear_button.Disable()

        self.queue_list_box.Clear()
        for experiment in experiments:
            self.queue_list_box.Append(experiment)

    def deselected(self, event):
        """
        Deselects the selected experiment, and tells the parent to render the default control panel
        :param event: The event that cause the call
        """
        self.GetParent().render_control_panel(None)
        if (not isinstance(event, wx.KeyEvent)) or event.GetKeyCode() == wx.WXK_ESCAPE:
            for selected in self.queue_list_box.GetSelections():
                self.queue_list_box.Deselect(selected)

    def selected(self, event):

        """
        Tells the parent to render the control panel with the selected experiment
        :param event: The event that caused the call
        """

        queue_manager = Globals.systemConfigManager.get_queue_manager()
        selected_experiment = queue_manager.get_ith_experiment(self.queue_list_box.GetSelection())
        self.GetParent().render_control_panel(selected_experiment)
        pass

    @staticmethod
    def run_the_queue(event):
        """
        Runs the queue.
        :param event: The triggering event.
        """
        ui_control = Globals.systemConfigManager.get_ui_controller()
        if ui_control is not None:
            ui_control.switch_queue_to_running()
        Globals.systemConfigManager.get_queue_manager().run()

    def clear_queue(self, event):
        """
        Clears the queue.
        :param event: The triggering event.
        """
        self.deselected(event)
        Globals.systemConfigManager.get_queue_manager().clear_queue()

        ui_control = Globals.systemConfigManager.get_ui_controller()
        ui_control.rebuild_queue_page()

    def save_queue(self, event):
        """
        Saves the queue.
        :param event: The triggering event.
        """
        st = self.save_text_box.GetValue().strip().replace(" ", "_")
        if os.path.isfile(os.path.join(SAVED_QUEUES_DIR, "Saved_Queue_" + st)):
            dialog = wx.MessageDialog(None, "A queue with that name already exists. Would you like to overwrite it?", "Overwrite Queue", wx.YES_NO | wx.NO_DEFAULT)
            result = dialog.ShowModal()
            if result == wx.ID_NO:
                return
        save_result = Globals.systemConfigManager.get_queue_manager().save_queue_to_file(SAVED_QUEUES_DIR, st)

        if save_result:
            print(("Queue saved: " + st))
            self.load_choice_box.Append(st.replace("_", " "))
            self.save_text_box.Clear()

    def load_queue(self, event):
        """
        Loads the queue in the load box after clearing what was currently in the queue.
        :param event: The triggering event.
        """
        self.deselected(event)
        Globals.systemConfigManager.get_queue_manager().clear_queue()

        saved_queue_name = self.load_choice_box.GetString(self.load_choice_box.GetSelection()).replace(" ", "_")

        queue_manager = Globals.systemConfigManager.get_queue_manager()
        experiments = queue_manager.read_queue_from_file(
            os.path.join(SAVED_QUEUES_DIR, "Saved_Queue_" + saved_queue_name)
        )

        # pretty much what add_experiment does, and it works well
        for experiment in experiments:
            queue_manager.add_to_queue(experiment)

        ui_control = Globals.systemConfigManager.get_ui_controller()
        ui_control.rebuild_queue_page()
        #

    def check_save_button_state(self, event):
        """
        When text has been entered anywhere in this UI component. Change the save button to visible or invisible
        :param event: The event object
        """
        # handle save queue box text entered
        in_text_box = self.save_text_box.GetLineText(0)
        if len(in_text_box) > 0:
            self.save_button.Enable()
        else:
            self.save_button.Disable()

    def check_load_button_state(self, event):
        """
        Enable the load queue button when the user selects a choice. The UI will start with no choices being selected
        :param event: The event object
        :return:
        """
        self.load_button.Enable()

    @staticmethod
    def get_loadable_queues():
        """
        Gets possible experiments to load.
        :return: A list of loadable experiments.
        """
        res = []
        try:
            for fl in os.listdir(SAVED_QUEUES_DIR):
                res.append(fl[12:].replace("_", " "))
        except WindowsError as e:
            if e.errno == 2:
                os.mkdir(SAVED_QUEUES_DIR)
            else:
                raise e
        return res
