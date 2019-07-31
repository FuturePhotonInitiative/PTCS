import wx
import json
import imp
import inspect

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

        self.param_line = wx.BoxSizer(wx.HORIZONTAL)
        self.param_text = wx.StaticText(self)
        self.param_text.SetLabelText("Function:  | Parameters: ")
        self.param_line.Add(self.param_text, wx.EXPAND | wx.ALL)

        self.items = []

        self.param_items = []

        self.lines = []

        self.update_valid = True

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.save_sizer, 1, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.list_box, 15, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.delete_button, 1, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.input_line, 1, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.param_line, 1, wx.EXPAND | wx.ALL)

        self.Bind(wx.EVT_LISTBOX, self.load_on_click)

        self.Bind(wx.EVT_TEXT, self.update_text)
        self.Bind(wx.EVT_CHOICE, self.update_on_choice)

        self.SetSizer(self.sizer)

        self.list_box.SetBackgroundColour(CONSTANTS.TEST_BUILD_PANEL_COLOR)
        self.list_box.SetForegroundColour(CONSTANTS.TEST_BUILD_PANEL_FOREGROUND_COLOR)

        self.reload()

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.deselected)

        self.device_functions = {}
        self.fcs = []
        self.fc_args = {}

        hwm = Globals.systemConfigManager.get_hardware_manager()
        for dev in hwm.get_all_hardware_names():
            drv = hwm.get_hardware_object(dev).driver
            drvcls = imp.load_source("drvcls", "../../src/Instruments/" + drv + ".py")
            classes = inspect.getmembers(drvcls, inspect.isclass)
            funcs = []
            for c in classes:
                if str(c[0]) == drv:
                    funcs = [m for m in inspect.getmembers(c[1], inspect.ismethod) if m[0][0] != "_"]
            self.device_functions[dev] = funcs
            for func in funcs:
                if func[0] not in [f[0] for f in self.fcs]:
                    self.fcs.append((func[0], len(inspect.getargspec(func[1])[0]) - 1, func[0]))
                    self.fc_args[func[0]] = inspect.getargspec(func[1])[0][1:]
        self.fcs.sort(key=lambda fn: fn[0], reverse=True)

    def save(self, event):
        ip = build.parse_input([p[0] for p in self.lines])
        test_name = self.save_field.GetLineText(0)
        test_v = test_name.replace(" ", "_")
        ip.insert(0, "Test- " + test_name)
        config, script = build.parse_lines(ip, test_v, self.fcs)
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
        self.check_param_display()

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

    def load_params(self, function):
        params = self.fc_args.get(function, [])
        # pvs = param_string.split(' ')
        # self.param_line.Clear(delete_windows=True)
        ptxt = "Function: " + function + " | Parameters: "
        dl = ""
        for i in range(len(params)):
            p = params[i]
            # pv = pvs[i]
            # b = wx.StaticText(self)
            # b.SetLabelText(p)
            # self.param_items.append(b)
            # self.param_line.Add(b, wx.EXPAND | wx.ALL)
            ptxt += dl + p
            dl = ", "

            # tx = wx.TextCtrl(self)
            # tx.SetLabelText(pv)
            # self.param_items.append(tx)
            # self.param_line.Add(tx, wx.EXPAND | wx.ALL)
        self.param_text.SetLabelText(ptxt)


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
            elif symbol == "[FNC]":
                b = wx.Choice(self)
                i = items[1].GetSelection()
                dev = ""
                if i > -1:
                    dev = items[1].GetString(i)
                for fc in self.device_functions.get(dev, []):
                    b.Append(fc[0])
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
        self.check_param_display()
        return output

    def delete_line(self, event):
        i = self.list_box.GetSelection()
        if i > -1:
            self.update_valid = False
            self.list_box.Deselect(i)
            self.list_box.Delete(i)
            self.lines.pop(i)
            self.load_input_line([])
            self.update_valid = True

    def load_input_line(self, line):
        self.input_line.Clear(delete_windows=True)
        for i in line:
            self.input_line.Add(i, wx.EXPAND | wx.ALL)
        self.sizer.Layout()
        self.items = line

    def update_text(self, event):
        lind = self.list_box.GetSelection()
        if self.update_valid:
            output = ""
            ind = 0
            if lind > -1 and len(self.lines[lind][0]) == len(self.items):
                for i in range(len(self.items)):
                    s = self.get_text(self.items[i], i)
                    output += s + " "
                    if lind > -1:
                        self.lines[lind][0][ind] = s
                    ind += 1
                if len(output) > 0:
                    output = output[:-1]
                if lind > -1:
                    self.list_box.SetString(lind, output)

    def update_functions(self, event):
        ob = event.GetEventObject()
        lind = self.list_box.GetSelection()
        if len(self.items) > 3 and len(self.lines[lind][1]) > 3 and lind > -1 and self.items[1] == ob \
                and self.lines[lind][1][3] == "[FNC]":
            i = self.items[1].GetSelection()
            dev = ""
            if i > -1:
                dev = self.items[1].GetString(i)
            self.items[3].Clear()
            for fc in self.device_functions.get(dev, []):
                self.items[3].Append(fc[0])
        if len(self.items) > 3 and len(self.lines[lind][1]) > 3 and lind > -1 and self.items[3] == ob \
                and self.lines[lind][1][3] == "[FNC]":
            self.check_param_display()

    def check_param_display(self):
        lind = self.list_box.GetSelection()
        if len(self.items) > 3 and len(self.lines[lind][1]) > 3 and lind > -1 and self.lines[lind][1][3] == "[FNC]":
            i = self.items[3].GetSelection()
            fnc = ""
            if i > -1:
                fnc = self.items[3].GetString(i)
            self.load_params(fnc)
        else:
            self.load_params("")

    def update_on_choice(self, event):
        self.update_functions(event)
        self.update_text(event)


    def get_text(self, item, index):
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
                elif index == 1:
                    s = "[DEV]"
                else:
                    s = "[FNC]"
            else:
                s = item.GetString(i)
        elif type(item) == wx.StaticText:
            s = item.GetLabel()
        return s
