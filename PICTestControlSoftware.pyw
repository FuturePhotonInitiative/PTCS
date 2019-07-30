"""
This is the file that should be run if running in standalone mode, or without pycharm's automatic
 project directory path addition.
All this does is add the project directory to the path and start the GUI.
Since this is also a .pyw file, when you create a shortcut to this file, no console will show up with the GUI
If src.GUI.GuiMainApp is run through a shortcut, it will fail because it cant find all the imports because the project
 directory is not in the python path
"""
import sys
from os.path import dirname

import src.GUI.GuiMainApp as GUIMainApp

if __name__ == "__main__":
    proj_dir = dirname(sys.argv[0])
    sys.path.append(proj_dir)
    GUIMainApp.main()
