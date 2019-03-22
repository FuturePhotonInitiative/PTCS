import wx

from src.GUI.Model.ExperimentModel import Experiment
from src.GUI.Model.ExperimentQueue import ExperimentQueue
from src.GUI.Model.HardwareModel import HardwareModel
from src.GUI.UI.MainFrame import MainFrame
import src.GUI.Util.Globals as Globals


if __name__ == '__main__':
    # TODO hardcoded config paths are bad and we can do better.
    Globals.ExperimentQueue = ExperimentQueue(['../../System/Devices.json', '../../System/Files.json'])
    Globals.Hardware = HardwareModel(['../../System/Devices.json', '../../System/Files.json'])
    # TODO temp testing code to make sure queue displays properly
    Globals.ExperimentQueue.add_to_queue(Experiment("../../Configs/Dummy_Test1.json"))
    Globals.ExperimentQueue.add_to_queue(Experiment("../../Configs/Dummy_Test2.json"))
    Globals.ExperimentQueue.add_to_queue(Experiment("../../Configs/Dummy_Test3.json"))
    Globals.ExperimentQueue.add_to_queue(Experiment("../../Configs/Dummy_Test4.json"))
    Globals.ExperimentQueue.add_to_queue(Experiment("../../Configs/Dummy_Test5.json"))
    app = wx.App()
    frame = MainFrame(None, -1)
    frame.Show()
    app.MainLoop()

