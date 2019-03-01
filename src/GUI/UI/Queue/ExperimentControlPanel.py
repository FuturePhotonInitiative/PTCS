import wx
import src.GUI.Util.GUI_CONSTANTS
import src.GUI.Model.ExperimentModel
import toStringTest


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
        self.choicebox = None

        self.render_with_experiment(experiment)

    def render_without_experiment(self):
        self.sizer.Clear(delete_windows=True)
        self.experiment = None
        self.variables_text_fields = []
        self.variables_labels = []
        self.variables_boxes = []

        self.choicebox = wx.Choice(self, choices=self.get_experiments())
        self.add_button = wx.Button(self, label="Add")
        self.sizer.Add(self.choicebox, 1, wx.SHAPED | wx.ALL | wx.ALIGN_CENTRE)
        self.sizer.Add(self.add_button, 1, wx.EXPAND | wx.ALL)

        self.sizer.Layout()

    def render_with_experiment(self, experiment):
        if experiment is not None and experiment != self.experiment:
            self.experiment = experiment
            self.sizer.Clear(delete_windows=True)
            self.variables_text_fields = []
            self.variables_labels = []
            self.variables_boxes = []
            for variable in self.experiment.get_data_keys():
                # print variable
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                text_feild = wx.TextCtrl(self, value=str(self.experiment.get_data_value(variable)))
                label = wx.StaticText(self, label=variable)

                hbox.Add(label, 1, wx.EXPAND | wx.ALL)
                hbox.Add(text_feild, 1, wx.EXPAND | wx.ALL)
                self.sizer.Add(hbox, 1, wx.EXPAND | wx.ALL)

                self.variables_labels.append(label)
                self.variables_text_fields.append(text_feild)
                self.variables_boxes.append(hbox)
            self.sizer.Layout()

        elif experiment is None:
            self.render_without_experiment()

    def get_experiments(self):
        return self.GetParent().get_experiments()

    def add_experements(self):
        self.choicebox.GetString()