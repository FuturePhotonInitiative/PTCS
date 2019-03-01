import wx
import src.GUI.Util.GUI_CONSTANTS
import src.GUI.Model.ExperimentModel
import src.GUI.Util.Globals as Globals


class ExperimentControlPanel(wx.StaticBox):
    def __init__(self, parent, experiment):
        wx.StaticBox.__init__(self, parent)

        self.SetBackgroundColour(src.GUI.Util.GUI_CONSTANTS.CONTROL_PANEL_COLOR)
        self.SetForegroundColour(src.GUI.Util.GUI_CONSTANTS.CONTROL_PANEL_FOREGROUND_COLOR)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.variables_text_fields = []
        self.variables_labels = []
        self.variables_boxes = []
        self.experiment = None

        self.experiments = []
        self.choice_box = None
        self.remove_button = None
        self.add_button = None



        self.render_with_experiment(experiment)

    def render_without_experiment(self):
        self.sizer.Clear(delete_windows=True)
        self.experiment = None
        self.variables_text_fields = {}
        self.variables_labels = {}
        self.variables_boxes = {}

        self.choice_box = wx.Choice(self, choices=self.get_experiments())
        self.add_button = wx.Button(self, label="Add")
        self.sizer.Add(self.choice_box, 1, wx.SHAPED | wx.ALL | wx.ALIGN_CENTRE)
        self.sizer.Add(self.add_button, 1, wx.EXPAND | wx.ALL)

        self.add_button.Bind(wx.EVT_BUTTON, self.add_experiment)
        self.sizer.Layout()

    def render_with_experiment(self, experiment):
        if experiment is not None and experiment != self.experiment:
            self.experiment = experiment
            self.sizer.Clear(delete_windows=True)
            self.variables_text_fields = {}
            self.variables_labels = {}
            self.variables_boxes = {}
            for variable in self.experiment.get_data_keys():
                # print variable
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                text_feild = wx.TextCtrl(self, value=str(self.experiment.get_data_value(variable)))
                label = wx.StaticText(self, label=variable)

                hbox.Add(label, 1, wx.EXPAND | wx.ALL)
                hbox.Add(text_feild, 1, wx.EXPAND | wx.ALL)
                self.sizer.Add(hbox, 1, wx.EXPAND | wx.ALL)

                self.variables_labels[variable] = label
                self.variables_text_fields[variable] = text_feild
                self.variables_boxes[variable] = hbox

                text_feild.Bind(wx.EVT_TEXT, self.update_variable, text_feild)

            self.remove_button = wx.Button(self, label="Remove")
            self.remove_button.Bind(wx.EVT_BUTTON, self.remove_experiment)
            self.sizer.Add(self.remove_button, 1, wx.EXPAND | wx.ALL)

            self.sizer.Layout()

        elif experiment is None:
            self.render_without_experiment()

    def update_variable(self, evt):
        for variable in self.experiment.get_data_keys():
            self.experiment.set_data_value(variable, self.variables_text_fields[variable].GetValue())

    def get_experiments(self):
        return self.GetParent().get_experiments()

    def add_experiment(self, evt):
        experiment = self.choice_box.GetString(self.choice_box.GetSelection())
        experiment = Globals.SPAE.get_experiment_from_name(experiment)
        if experiment:
            Globals.SPAE.add_to_queue(experiment)
            self.GetParent().reload()

    def remove_experiment(self, evt):
        if self.experiment:
            Globals.SPAE.remove_from_queue(self.experiment)
            self.render_without_experiment()
            self.GetParent().reload()