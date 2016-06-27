import Tkinter as Tk
import os

class NPS_root(Tk.Tk):
    def __init__(self, *args, **kwargs):
        Tk.Tk.__init__(self, *args, **kwargs)
        self.title ('NPS CLIMATE DATABASE APPLICATION')
        self.iconbitmap(os.path.dirname(__file__) + '\\NPS.ico')
        return

if __name__ == '__main__':
    app = NPS_root()
    app.mainloop()