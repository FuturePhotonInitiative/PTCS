import wx
import src.GUI.Util.GUI_CONSTANTS
import src.GUI.Model.ExperimentModel
import src.GUI.Util.Globals as Globals
from src.GUI.UI.SpaeControlPanel import SpaeControlPanel


class ExperimentControlPanel(SpaeControlPanel):
    """
    A panel for viewing and modifying the variables in an experiment
    """

    def __init__(self, parent, experiment=None):
        """
        Sets up an experiment control panel
        :param parent: The parent to display the panel on
        :param experiment: The experiment to use when rendering
        """
        SpaeControlPanel.__init__(self, parent)


        self.UI_control = Globals.systemConfigManager.get_ui_controller()

        # Sets up the colors display Constants are in Util.CONSTANTS
        self.SetBackgroundColour(src.GUI.Util.GUI_CONSTANTS.CONTROL_PANEL_COLOR)
        self.SetForegroundColour(src.GUI.Util.GUI_CONSTANTS.CONTROL_PANEL_FOREGROUND_COLOR)

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

        # Renders the panel with the given experiment
        self.render(experiment)

    def set_up_ui_control(self, ui_control):
        if ui_control is None:
            ui_control = Globals.systemConfigManager.get_ui_controller()
        if ui_control:
            controls_to_add = []

            controls_to_add.extend(self.variables_labels)

            controls_to_add.append(self.choice_box)
            controls_to_add.append(self.remove_button)
            controls_to_add.append(self.add_button)
            print "ADD BUTTON:", self.add_button


            for control in controls_to_add:
                ui_control.add_control_to_text_list(control)

    def clean_up_ui_control(self):
        ui_control = Globals.systemConfigManager.get_ui_controller()
        if ui_control:
            controls_to_add = []

            controls_to_add.extend(self.variables_labels)

            controls_to_add.append(self.choice_box)
            controls_to_add.append(self.remove_button)
            controls_to_add.append(self.add_button)

            for control in controls_to_add:
                ui_control.remove_control_from_text_list(control)

    def render(self, experiment):
        """
        Sets up the panel with an experiment and it's components
        :param experiment: The experiment to render the page with
        """
        self.clean_up_ui_control()
        if experiment is not None and experiment != self.experiment:

            # Set the new experiment to the experiment to be worked with
            self.experiment = experiment

            # Clear out the components from the old experiment
            self.sizer.Clear(delete_windows=True)
            self.variables_text_fields = {}
            self.variables_labels = {}
            self.variables_boxes = {}

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

            # Add a remove button at the bottom of the page
            self.sizer.Add(self.remove_button, 1, wx.EXPAND | wx.ALL)

            self.sizer.Layout()

        elif experiment is None:
            # if there is no experiment given, render with no experiment
            self.render_without_experiment()
        self.set_up_ui_control(None)

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
        self.choice_box = wx.Choice(self, choices=Globals.systemConfigManager.get_experiments_manager().get_available_experiments_names())
        # self.UI_control.add_control_to_text_list(self.choice_box)
        self.add_button = wx.Button(self, label="Add")
        # self.UI_control.add_control_to_text_list(self.add_button)
        self.sizer.Add(self.choice_box, 1, wx.SHAPED | wx.ALL | wx.ALIGN_CENTRE)
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

