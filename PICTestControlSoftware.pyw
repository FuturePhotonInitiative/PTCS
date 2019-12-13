"""
This is the main file that should be run to start the program
Since this is a .pyw file, when you create a shortcut to this file, no console will show up with the GUI
"""

import matplotlib
import sys

# if there are args on the command line, you probably just want to run a config file
if __name__ == "__main__":
    # matplotlib backend needs to be changed because of GitHub issue #20
    matplotlib.use("WXAgg")
    if len(sys.argv) > 1:
        import src.GUI.RunAConfigFileMain as RunAConfigFileMain
        RunAConfigFileMain.main(sys.argv)
    else:
        import src.GUI.GuiMainApp as GUIMainApp
        GUIMainApp.main()