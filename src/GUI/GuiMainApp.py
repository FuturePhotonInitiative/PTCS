import wx

from src.GUI.Application.SystemConfigManager import SystemConfigManager
from src.GUI.UI.MainFrame import MainFrame
import src.GUI.Util.Globals as Globals


if __name__ == '__main__':
    Globals.systemConfigManager = SystemConfigManager()
    app = wx.App()
    frame = MainFrame(None, -1)
    Globals.systemConfigManager.mainframe = frame
    frame.Show()
    app.MainLoop()

