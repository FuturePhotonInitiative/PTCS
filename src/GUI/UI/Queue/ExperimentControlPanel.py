import wx
import os

from src.GUI.Util import CONSTANTS
import src.GUI.Util.Globals as Globals
from src.GUI.UI.ControlPanel import ControlPanel


class ExperimentControlPanel(ControlPanel):
    """
    A panel for viewing and modifying the variables in an experiment
    """

    def __init__(self, parent, experiment=None):
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

        # Sets up the dictionaries for the variable's display components
        self.variables_text_fields = {}
        self.variables_labels = {}
        self.variables_boxes = {}

        # Sets the experiment to the default value
        self.experiment = None

        # Declaring the controls for the default panel
        self.choice_box = None
        self.remove_button = None
        self.add_button = None
        self.show_source_button = None

        # Renders the panel with the given experiment
        self.render(experiment)

    def render(self, experiment):
        """
        Sets up the panel with an experiment and it's components
        :param experiment: The experiment to render the page with
        """
        if experiment is not None and experiment != self.experiment:

            # Set the new experiment to the experiment to be worked with
            self.experiment = experiment

            # Clear out the components from the old experiment
            self.sizer.Clear(delete_windows=True)
            self.variables_text_fields = {}
            self.variables_labels = {}
            self.variables_boxes = {}

            # Display test description in the config file
            if experiment.get_description:
                desc_header = wx.StaticText(self, label="Test Description")
                desc_header.SetFont(wx.Font().Bold())
                self.sizer.Add(desc_header, 0, wx.ALIGN_CENTER | wx.ALL)
                description_box = wx.StaticText(self, label=experiment.get_description())
                description_box.Wrap(self.GetSize().width)
                self.sizer.Add(description_box, 0, wx.EXPAND | wx.ALL)

            # Display the instruments used in this test
            devices_header = wx.StaticText(self, label="Devices Used")
            devices_header.SetFont(wx.Font().Bold())
            self.sizer.Add(devices_header, 0, wx.ALIGN_CENTER | wx.ALL)

            devices_used = experiment.get_devices()
            if devices_used:
                for device in devices_used:
                    self.sizer.Add(wx.StaticText(self, label=device), 0, wx.ALL)
            else:
                self.sizer.Add(wx.StaticText(self, label="No devices used"), 0, wx.ALL)

            # Display the parameters able to be configured for this test
            params_header = wx.StaticText(self, label="Configurable Parameters")
            params_header.SetFont(wx.Font().Bold())
            self.sizer.Add(params_header, 0, wx.ALIGN_CENTER | wx.ALL)

            # Add components (A Label and Textbox) for each of the experiments variables
            for variable in self.experiment.get_data_keys():

                # Set up label and text field
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                text_feild = wx.TextCtrl(self, value=str(self.experiment.get_data_value(variable)))
                # self.UI_control.add_control_to_text_list(text_feild)
                label = wx.StaticText(self, label=variable)
                # self.UI_control.add_control_to_text_list(label)

                # Add the components to the sizers
                hbox.Add(label, 1, wx.EXPAND | wx.ALL)
                hbox.Add(text_feild, 1, wx.EXPAND | wx.ALL)
                self.sizer.Add(hbox, 1, wx.EXPAND | wx.ALL)

                # Add the components to their dictionaries
                self.variables_labels[variable] = label
                self.variables_text_fields[variable] = text_feild
                self.variables_boxes[variable] = hbox

                # Bind the update variable function for when a variable is edited
                text_feild.Bind(wx.EVT_TEXT, self.update_variable, text_feild)

            # Set up remove button
            self.remove_button = wx.Button(self, label="Remove")
            # self.UI_control.add_control_to_text_list(self.remove_button)

            # Bind the remove button to a remove function
            self.remove_button.Bind(wx.EVT_BUTTON, self.remove_experiment)

            # Set up show source button
            self.show_source_button = wx.Button(self, label="Show Source")

            # Bind the show source button to a show source function
            self.show_source_button.Bind(wx.EVT_BUTTON, self.show_source)

            self.sizer.Add(self.show_source_button, 0.5, wx.EXPAND | wx.ALL)

            exp_name = self.experiment.get_name().replace(" ", "_")
            if not os.path.isfile("Custom_Tests/" + exp_name + ".txt"):
                self.show_source_button.Disable()

            # Add a remove button at the bottom of the page
            self.sizer.Add(self.remove_button, 1, wx.EXPAND | wx.ALL)

            self.sizer.Layout()

        elif experiment is None:
            # if there is no experiment given, render with no experiment
            self.render_without_experiment()

    def render_without_experiment(self):
        """
        Renders the panel with the default setup which allows for adding an experiment to the queue
        """

        # Clears out the old experiment and it's components
        self.sizer.Clear(delete_windows=True)
        self.experiment = None
        self.variables_text_fields = {}
        self.variables_labels = {}
        self.variables_boxes = {}

        # Sets up default page
        self.label = wx.StaticText(self)
        self.label.SetLabelText("Pre-Defined Tests")
        self.label.SetFont(wx.Font(wx.FontInfo(30)))
        self.choice_box = wx.Choice(self,
                    choices=Globals.systemConfigManager.get_experiments_manager().get_available_experiments_names())
        self.choice_box.SetFont(wx.Font(wx.FontInfo(22)))
        # self.UI_control.add_control_to_text_list(self.choice_box)
        self.add_button = wx.Button(self, label="Add")
        self.add_button.SetFont(wx.Font(wx.FontInfo(30)))
        # self.UI_control.add_control_to_text_list(self.add_button)
        self.sizer.Add(self.label, 1, wx.ALIGN_BOTTOM)
        self.sizer.Add(self.choice_box, 1, wx.SHAPED | wx.ALL)
        self.sizer.Add(self.add_button, 1, wx.EXPAND | wx.ALL)

        self.add_button.Bind(wx.EVT_BUTTON, self.add_experiment)
        self.sizer.Layout()
        # self.UI_control.fix_control_list()

    def update_variable(self, evt):
        """
        Handles editing variables
        :param evt: The causing event
        """
        for variable in self.experiment.get_data_keys():
            self.experiment.set_data_value(variable, self.variables_text_fields[variable].GetValue())

    def add_experiment(self, evt):
        """
        Adds an experiment to the queue
        :param evt: The causing event
        """
        experiment = self.choice_box.GetString(self.choice_box.GetSelection())
        experiment = Globals.systemConfigManager.get_experiments_manager().get_experiment_from_name(experiment)
        if experiment:
            Globals.systemConfigManager.get_queue_manager().add_to_queue(experiment)

            ui_control = Globals.systemConfigManager.get_ui_controller()
            ui_control.rebuild_queue_page()

    def remove_experiment(self, evt):
        """
        Removes an experiment from the queue
        :param evt: The causing event
        """
        if self.experiment:
            Globals.systemConfigManager.get_queue_manager().remove_from_queue(self.experiment)
            self.render_without_experiment()

            ui_control = Globals.systemConfigManager.get_ui_controller()
            ui_control.rebuild_queue_page()

    def show_source(self, evt):
        exp_name = self.experiment.get_name().replace(" ", "_")
        os.system("start Custom_Tests/" + exp_name + ".txt")
