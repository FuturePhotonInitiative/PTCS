import wx

import src.GUI.Util.GUI_CONSTANTS
import src.GUI.Util.Globals as Globals
from src.GUI.UI.ControlPanel import ControlPanel


class TestButtonPanel(ControlPanel):
    def __init__(self, parent):
        ControlPanel.__init__(self, parent)

        self.build_panel = parent.build_panel

        self.build_panel.__init__(parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        names = ["IF", "ELSE", "END", "LOOP", "PARAMETER", "SET", "PRINT",
                 "DEVICE", "SAVE", "START TIMER", "GET TIMER", "DEVICE CALL", "DEVICE READ"]

        patterns = [["IF", "[STR]", "[OP]", "[STR]"],
                    ["ELSE"],
                    ["END"],
                    ["LOOP WHILE", "[STR]", "[OP]", "[STR]"],
                    ["PARAMETER", "[STR]", "[STR]"],
                    ["SET", "[STR]", "=", "[STR]"],
                    ["PRINT", "[STR]"],
                    ["IMPORT", "[DEV]", "AS", "[STR]"],
                    ["SAVE", "[STR]", ",", "[STR]"],
                    ["START TIMER"],
                    ["GET TIMER AS", "[STR]"],
                    ["FROM", "[STR]", "CALL", "[FNC]", "[STR]"],
                    ["FROM", "[STR]", "READ", "[FNC]", "[STR]", "AS", "[STR]"]]

        self.buttons = self.add_buttons(self.sizer, names, 4)

        for i in range(len(names)):
            self.buttons[i].Bind(wx.EVT_BUTTON, (lambda label: lambda evt:
                self.build_panel.add_symbol(evt, label))(patterns[i]))

        self.SetSizer(self.sizer)



    def add_buttons(self, sizer, names, columns):
        lst = []
        rows = [wx.BoxSizer(wx.HORIZONTAL)]
        colct = 0
        for name in names:
            if colct == columns:
                sizer.Add(rows[len(rows) - 1], 1, wx.EXPAND | wx.ALL)
                rows.append(wx.BoxSizer(wx.HORIZONTAL))
                colct = 0
            b = wx.Button(self)
            b.SetLabelText(name)
            rows[len(rows) - 1].Add(b, 1, wx.EXPAND | wx.ALL)
            lst.append(b)
            b.Bind(wx.EVT_BUTTON, lambda evt: self.build_panel.add_symbol(evt, name))
            colct += 1
        sizer.Add(rows[len(rows) - 1], 1, wx.EXPAND | wx.ALL)
        return lst