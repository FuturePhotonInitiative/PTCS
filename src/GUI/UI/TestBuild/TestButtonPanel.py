import wx

from src.GUI.UI.ControlPanel import ControlPanel


class TestButtonPanel(ControlPanel):
    """
    Panel for rendering the buttons required to build a test.
    """
    def __init__(self, parent, hardware_manager):
        """
        Set up the Test Button Panel.
        :param parent: The parent to display the panel on
        """
        ControlPanel.__init__(self, parent)

        self.build_panel = parent.build_panel

        self.build_panel.__init__(parent, hardware_manager)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Button names
        names = ["IF", "ELSE", "END", "LOOP", "PARAMETER", "SET", "PRINT",
                 "SAVE", "START TIMER", "GET TIMER", "DEVICE CALL", "DEVICE READ"]

        # Button patterns
        patterns = [["IF", "[STR]", "[OP]", "[STR]"],
                    ["ELSE"],
                    ["END"],
                    ["LOOP WHILE", "[STR]", "[OP]", "[STR]"],
                    ["PARAMETER", "[STR]", "[STR]"],
                    ["SET", "[STR]", "=", "[STR]"],
                    ["PRINT", "[STR]"],
                    ["SAVE", "[STR]", ",", "[STR]"],
                    ["START TIMER"],
                    ["GET TIMER AS", "[STR]"],
                    ["FROM", "[DEV]", "CALL", "[FNC]", "[STR]"],
                    ["FROM", "[DEV]", "READ", "[FNC]", "[STR]", "AS", "[STR]"]]

        self.buttons = self.add_buttons(self.sizer, names, 4)

        for i in range(len(names)):
            self.buttons[i].Bind(wx.EVT_BUTTON, (lambda label: lambda evt:
                self.build_panel.add_symbol(evt, label))(patterns[i]))

        self.SetSizer(self.sizer)

    def add_buttons(self, sizer, names, columns):
        """
        Add buttons to the panel.
        :param sizer: Sizer to add to.
        :param names: Button names.
        :param columns: Number of columns.
        :return: The list of buttons.
        """
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
