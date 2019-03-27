import wx
import src.GUI.Util.GUI_CONSTANTS as CONSTANTS


class BuildExperimentsPage(wx.Panel):
    """

    """

    def __init__(self, parent):
        """
        Sets up the Build Experiment Page
        The page has two sections
        The first section is the scripts panel, which will display the lego like pieces for making an experiment
        The second section is the experiment panel,
            which will hold a field for building an experiment by linking lego like scripts together
        :param parent: The wxframe that the Build Experiment Page will be shown on
        """
        wx.Panel.__init__(self, parent)

        # sets up the sub-sections
        self.experiments_panel = wx.StaticBox(self)
        self.scripts_panel = wx.StaticBox(self)

        # adds the subsections to the page
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.scripts_panel, CONSTANTS.BUILD_SCRIPT_PANEL_PROPORTION, wx.EXPAND)
        sizer.Add(self.experiments_panel, CONSTANTS.BUILD_PANEL_PROPORTION, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Layout()
