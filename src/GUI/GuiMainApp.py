import wx

from src.GUI.Model.ExperimentModel import Experiment
from src.GUI.Model.SPAEModel import SPAEModel
from src.GUI.UI.MainFrame import MainFrame
import src.GUI.UI.Globals as Globals


if __name__ == '__main__':
    # TODO hardcoded config paths are bad and we can do better.
    Globals.SPAE = SPAEModel(['../../System/Devices.json'])
    # TODO temp testing code to make sure queue displays properly
    Globals.SPAE.add_to_queue(Experiment("../../Configs/Dummy_Test1.json"))
    Globals.SPAE.add_to_queue(Experiment("../../Configs/Dummy_Test2.json"))
    Globals.SPAE.add_to_queue(Experiment("../../Configs/Dummy_Test3.json"))
    Globals.SPAE.add_to_queue(Experiment("../../Configs/Dummy_Test4.json"))
    Globals.SPAE.add_to_queue(Experiment("../../Configs/Dummy_Test5.json"))
    app = wx.App()
    frame = MainFrame(None, -1)
    frame.Show()
    app.MainLoop()

