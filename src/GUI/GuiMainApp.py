import wx
from src.Gui.UI.MainFrame import MainFrame

if __name__ == '__main__':
    app=wx.App()
    frame = MainFrame(None, -1)
    frame.Show()
    app.MainLoop()

