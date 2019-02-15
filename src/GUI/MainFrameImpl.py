from MainFrame import MainFrame


class MainFrameImpl (MainFrame):
	def __init__(self, *args, **kwds):
		MainFrame.__init__(self, *args, **kwds)

	def OnListClick(self, event):
		selectedItem = str(event.GetString())
		pass

	def OnMoveDownListPress(self, event):
		currentItemList = self.queue_list.GetItems()

		self.queue_list.Set()
		pass

	def OnMoveUpListPress(self, event):
		pass

	def OnMenuAddExperiment(self, event):
		pass

	selectedItem = None
