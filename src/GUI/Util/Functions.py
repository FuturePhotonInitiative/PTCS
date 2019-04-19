import wx


def clean_name_for_file(name):
    OK_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    name_new = ""
    for letter in name:
        if letter not in OK_LETTERS:
            name_new += "_"
        else:
            name_new += letter
    return name_new

def fix_text_size(control, margin):
    try:
        font = control.GetFont()
        # print font
        # size = wx.Size(control.GetSize().Get()[1] / 4, control.GetSize().Get()[1] / 4)
        # print size
        wx.Font.Scale(font, round((float(control.GetSize().Get()[1] - margin) /
        float(font.GetPixelSize()[1]))/2.0))
        # wx.Font.SetPixelSize(font, size)
        dc = wx.ScreenDC()
        dc.SetFont(font)
        w, h = dc.GetTextExtent("test string")
        if w + margin > control.GetSize().Get()[0] and \
                control.GetSize().Get()[0] * (float(control.GetSize().Get()[0] - margin) / float(w)) > 0:
            # print 2
            scale = round(float(control.GetSize().Get()[0] - margin) / float(w), 2)
            wx.Font.Scale(font, scale)
            # print scale
        control.SetFont(font)
    except Exception as e:
        pass