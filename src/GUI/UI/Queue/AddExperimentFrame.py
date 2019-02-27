#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.0 on Mon Feb 04 15:57:48 2019
#

import json
import os
import wx
import src.Prober


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1290, 530))
        self.Choose_Test = wx.ComboBox(self, wx.ID_ANY, choices=os.listdir("../Configs"),
                                       style=wx.CB_DROPDOWN | wx.CB_SORT)
        self.Test_Name = wx.TextCtrl(self, wx.ID_ANY, "Default")
        self.Test_Name.Bind(wx.EVT_TEXT, self.on_key_typed_header)
        self.Run_Button = wx.Button(self, wx.ID_ANY, "RUN")
        self.Choose_Test.Bind(wx.EVT_COMBOBOX, self.on_select)
        self.Run_Button.Bind(wx.EVT_BUTTON, self.run_prober)

        # self.Config is the test configuration file
        self.Config = {}
        self.Variables = []
        self.Variable_Names = []
        count = 0
        while count < 10:
            self.Variable_Names.append(wx.StaticText(self, count, "Name"))
            self.Variables.append(wx.TextCtrl(self, count, "Default"))
            self.Variables[count].Bind(wx.EVT_TEXT, self.on_key_typed_variables, id=count)
            count += 1

        self.__set_properties()
        self.__do_layout()
    # end wxGlade

    def on_key_typed_variables(self, event):
        # begin on_key_typed_variables
        self.Config["Data"][self.Variable_Names[event.GetId()].GetLabelText()] = event.GetString()

    # end on_key_typed_variables

    def on_key_typed_header(self, event):
        # begin on_key_typed_header
        self.Config["Name"] = event.GetString()

    # end on_key_typed_header

    def on_select(self, event):
        # begin on_select

        # Hide all variables to start
        count = 0
        while count < len(self.Variables):
            self.Variables[count].Hide()
            self.Variable_Names[count].Hide()
            count += 1

        # Go to test configuration and pull variables for test
        with open("../Configs/"+self.Choose_Test.GetStringSelection()) as selection:
            self.Config = json.load(selection)

        # Set name of test from Default to the default test name
        try:
            self.Test_Name.SetLabelText(self.Config["Name"])
        except KeyError:
            print "No name provided. Please enter a test name."

        # Show variables from test
        count = 0
        try:
            for variable in self.Config["Data"]:
                self.Variable_Names[count].SetLabelText(variable)
                self.Variable_Names[count].Show()
                self.Variables[count].SetLabelText(str(self.Config["Data"][variable]))
                self.Variables[count].Show()
                count += 1
        except KeyError:
            print "There is no data necessary for this test."

    # end on_select

    def run_prober(self, event):
        # begin run_prober
        print "Running \""+self.Test_Name.GetLabelText()+"\"..."

        # Create new json file based on updated variables called temp.json
        with open("temp.json", "w+") as temp:
            temp.write(json.dumps(self.Config, separators=(',', ": "), indent=4))

        # Prober.main takes in sys.argv when running from the command line
        # This string is intended to maintain the same format as running from the command line
        src.Prober.main(["Prober.py", "temp.json"])
    # Close the window after running the experiment?
    # self.Close()
    # end run_prober

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("frame")
        self.Choose_Test.SetMinSize((400, 25))
        self.Test_Name.SetMinSize((225, 25))
        self.Run_Button.SetMinSize((90, 45))
        self.Run_Button.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "Segoe UI"))
        for variable in sorted(self.Variables):
            variable.SetMinSize((75, 25))
            variable.Hide()
        for variable in sorted(self.Variable_Names):
            variable.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "Segoe UI"))
            variable.Hide()

    # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_1 = wx.GridSizer(11, 6, 0, 2)
        sizer_1.Add(self.Choose_Test, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_1.Add((0, 0), 0, 0, 0)
        sizer_1.Add((0, 0), 0, 0, 0)
        test_batch_name = wx.StaticText(self, wx.ID_ANY, "Test Batch Name :")
        test_batch_name.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_1.Add(test_batch_name, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        sizer_1.Add(self.Test_Name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_1.Add(self.Run_Button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        count = 0
        while count < 10:
            sizer_1.Add(self.Variable_Names[count], 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 0)
            sizer_1.Add(self.Variables[count], 0, wx.ALIGN_CENTER_VERTICAL, 0)
            sizer_1.Add((0, 0), 0, 0, 0)
            sizer_1.Add((0, 0), 0, 0, 0)
            sizer_1.Add((0, 0), 0, 0, 0)
            sizer_1.Add((0, 0), 0, 0, 0)
            count += 1

        self.SetSizer(sizer_1)
        self.Layout()
    # end wxGlade

# end of class MainFrame


class SPAE_GUI(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


# end of class SPAE_GUI


if __name__ == "__main__":
    SPAE_GUI = SPAE_GUI(0)
    SPAE_GUI.MainLoop()
