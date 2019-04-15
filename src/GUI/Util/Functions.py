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
        size = wx.Size(control.GetSize().Get()[1] / 2, control.GetSize().Get()[1] / 2)
        # print size
        wx.Font.SetPixelSize(font, size)
        dc = wx.ScreenDC()
        dc.SetFont(font)
        w, h = dc.GetTextExtent("test string")
        if w + margin > control.GetSize().Get()[-0] and \
                control.GetSize().Get()[-0] * (control.GetSize().Get()[-0] - margin / w) > 0:
            scale = (control.GetSize().Get()[-0] - margin) / w
            size = size.Scale(scale, scale)
            wx.Font.SetPixelSize(font, size)
        control.SetFont(font)
    except Exception as e:
        pass