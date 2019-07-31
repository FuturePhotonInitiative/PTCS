import wx
import json

from src.GUI.UI.DisplayPanel import DisplayPanel
from src.GUI.Util import CONSTANTS
import src.GUI.Model.TestBuildModel as build
import src.GUI.Util.Globals as Globals


class TestBuildPanel(DisplayPanel):
    def __init__(self, parent):
        DisplayPanel.__init__(self, parent)

        self.save_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.save_button = wx.Button(self)
        self.save_button.SetLabelText("Save As")
        self.save_button.Bind(wx.EVT_BUTTON, self.save)
        self.save_field = wx.TextCtrl(self)
        self.save_sizer.Add(self.save_button, wx.EXPAND | wx.ALL)
        self.save_sizer.Add(self.save_field, wx.EXPAND | wx.ALL)

        self.list_box = wx.ListBox(self)

        self.delete_button = wx.Button(self)
        self.delete_button.SetLabelText("Delete")
        self.delete_button.Bind(wx.EVT_BUTTON, self.delete_line)

        self.input_line = wx.BoxSizer(wx.HORIZONTAL)

        self.items = []

        self.lines = []

        self.update_valid = True

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.save_sizer, 1, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.list_box, 15, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.delete_button, 1, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.input_line, 1, wx.EXPAND | wx.ALL)

        self.Bind(wx.EVT_LISTBOX, self.load_on_click)

        self.Bind(wx.EVT_TEXT, self.update_text)
        self.Bind(wx.EVT_CHOICE, self.update_text)

        self.SetSizer(self.sizer)

        self.list_box.SetBackgroundColour(CONSTANTS.TEST_BUILD_PANEL_COLOR)
        self.list_box.SetForegroundColour(CONSTANTS.TEST_BUILD_PANEL_FOREGROUND_COLOR)

        self.reload()

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.deselected)

    def save(self, event):
        ip = build.parse_input([p[0] for p in self.lines])
        test_name = self.save_field.GetLineText(0)
        test_v = test_name.replace(" ", "_")
        ip.insert(0, "Test- " + test_name)
        config, script = build.parse_lines(ip, test_v)
        with open("../../Configs/" + test_v + ".json", "w") as f:
            json.dump(config, f)
        with open("../../src/Scripts/" + test_v + ".py", "w") as f:
            f.write(script)
        with open("../../Custom_Tests/" + test_v + ".txt", "w") as f:
            f.writelines([l + "\n" for l in ip])
        self.save_field.Clear()

    def deselected(self, event):
        i = self.list_box.GetSelection()
        if i > -1:
            self.list_box.Deselect(i)

    def add_symbol(self, event, pattern):
        output = self.get_load_output(pattern)

        i = self.list_box.GetSelection()
        if i > -1:
            self.list_box.Insert(output, i)
            self.lines.insert(i, [[k.replace("[STR]", "???").replace("[OP]", "-?-") for k in pattern], pattern])
        else:
            self.list_box.Append(output)
            self.lines.append([[k.replace("[STR]", "???").replace("[OP]", "-?-") for k in pattern], pattern])

    def load_on_click(self, event):
        i = self.list_box.GetSelection()
        output = self.load_symbol(self.lines[i])

    def get_load_output(self, pattern):
        output = ""
        for i in range(0, len(pattern)):
            symbol = pattern[i]
            if symbol == "[STR]":
                output += "??? "
            elif symbol == "[OP]":
                output += "-?- "
            else:
                output += symbol + " "
        output = output[:-1]
        return output

    def load_symbol(self, patterns):
        self.update_valid = False
        items = []
        output = ""
        self.input_line.Clear(delete_windows=True)
        for i in range(0, len(patterns[1])):
            symbol = patterns[1][i]
            if symbol == "[STR]":
                b = wx.TextCtrl(self)
                b.SetLabelText(patterns[0][i].replace("???", ""))
                items.append(b)
                output += patterns[0][i] + " "
            elif symbol == "[OP]":
                b = wx.Choice(self)
                b.Append(["==", "/=", "<", ">", "<=", ">="])
                si = b.FindString(patterns[0][i])
                if si > -1:
                    b.SetSelection(si)
                items.append(b)
                output += patterns[0][i] + " "
            elif symbol == "[DEV]":
                b = wx.Choice(self)
                b.Append(Globals.systemConfigManager.get_hardware_manager().get_all_hardware_names())
                si = b.FindString(patterns[0][i])
                if si > -1:
                    b.SetSelection(si)
                items.append(b)
                output += patterns[0][i] + " "
            else:
                b = wx.StaticText(self)
                b.SetLabelText(symbol)
                items.append(b)
                output += symbol + " "
        output = output[:-1]
        self.items = items
        self.load_input_line(items)
        self.update_valid = True
        self.update_text(None)
        return output

    def delete_line(self, event):
        i = self.list_box.GetSelection()
        if i > -1:
            self.update_valid = False
            self.list_box.Delete(i)
            self.lines.pop(i)
            self.list_box.Deselect(i)
            self.load_input_line([])
            self.update_valid = True

    def load_input_line(self, line):
        self.input_line.Clear(delete_windows=True)
        for i in line:
            self.input_line.Add(i, wx.EXPAND | wx.ALL)
        self.sizer.Layout()
        self.items = line

    def update_text(self, event):
        if self.update_valid:
            output = ""
            ind = 0
            lind = self.list_box.GetSelection()
            if lind > -1 and len(self.lines[lind][0]) == len(self.items):
                for i in self.items:
                    s = self.get_text(i)
                    output += s + " "
                    if lind > -1:
                        self.lines[lind][0][ind] = s
                    ind += 1
                if len(output) > 0:
                    output = output[:-1]
                if lind > -1:
                    self.list_box.SetString(lind, output)

    def get_text(self, item):
        s = ""
        if type(item) == wx.TextCtrl:
            s = item.GetLineText(0)
            if s == "":
                s = "???"
        elif type(item) == wx.Choice:
            i = item.GetSelection()
            if i == -1:
                if item.GetCount() > 0 and item.GetString(0) == "==":
                    s = "-?-"
                else:
                    s = "[DEV]"
            else:
                s = item.GetString(i)
        elif type(item) == wx.StaticText:
            s = item.GetLabel()
        return s
