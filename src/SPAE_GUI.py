import wx
from GUI.MainFrameImpl import MainFrameImpl


class SPAE_GUI (wx.App):

	def OnInit(self):
		self.main = MainFrameImpl(None, title="SPAE")
		self.SetTopWindow(self.main)
		self.main.Show()
		return True


if __name__ == '__main__':
	spae_app = SPAE_GUI()
	spae_app.MainLoop()
