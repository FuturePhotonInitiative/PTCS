import wx

from Application.SystemConfigManager import SystemConfigManager
from UI.MainFrame import MainFrame
import Util.Globals as Globals


def main():
    Globals.systemConfigManager = SystemConfigManager()
    app = wx.App()
    frame = MainFrame(None, -1)
    Globals.systemConfigManager.mainframe = frame
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
