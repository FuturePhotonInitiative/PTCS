import wx

from src.GUI.Application.SystemConfigManager import SystemConfigManager
from src.GUI.UI.MainFrame import MainFrame
import src.GUI.Util.Globals as Globals


if __name__ == '__main__':
    # TODO hardcoded config paths are bad and we can do better.
    Globals.systemConfigManager = SystemConfigManager('../../System/Files.json')
    # TODO temp testing code to make sure queue displays properly
    app = wx.App()
    frame = MainFrame(None, -1)
    frame.Show()
    app.MainLoop()

