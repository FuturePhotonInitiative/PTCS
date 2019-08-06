import wx

from UI.MainFrame import MainFrame


def main():
    app = wx.App()
    frame = MainFrame(None, -1)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
