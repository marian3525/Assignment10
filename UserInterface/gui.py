import wx

class GUI(wx.Frame):
    def __init__(self):
        app = wx.App(False)
        frame = wx.Frame(None, wx.ID_ANY, "Planes")
        frame.Show(True)
        app.MainLoop()
