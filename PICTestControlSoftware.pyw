"""
This is the file that should be run if running in standalone mode
Since this is a .pyw file, when you create a shortcut to this file, no console will show up with the GUI
"""

import matplotlib

# matplotlib backend needs to be changed because of GitHub issue #20
matplotlib.use("WXAgg")

if __name__ == "__main__":
    import src.GUI.GuiMainApp as GUIMainApp
    GUIMainApp.main()
