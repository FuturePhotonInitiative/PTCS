import wx

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

if __name__ == '__main__':
    from Application.SystemConfigManager import SystemConfigManager
    from UI.MainFrame import MainFrame
    import src.GUI.Util.Globals as Globals

    Globals.systemConfigManager = SystemConfigManager()
    app = wx.App()
    frame = MainFrame(None, -1)
    Globals.systemConfigManager.mainframe = frame
    frame.Show()
    app.MainLoop()
