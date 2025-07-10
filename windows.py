from tkinter import Tk, Toplevel
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo, askyesno

class _window:
    def configBorders(self, app, kind, iconfile):
        title = app
        if kind: title += " - " + kind
        self.title(title)
        self.iconname(app)
        if iconfile:
            try:
                image = Image.open(iconfile)
                photo = ImageTk.PhotoImage(image)
                self.iconphoto(True, photo)
            except:
                pass
        self.protocol("WM_DELETE_WINDOW", self.quit)
        
class MainWindow(Tk, _window):
    def __init__(self, app, kind='', iconfile=None):
        Tk.__init__(self)
        self.__app = app
        self.configBorders(app, kind, iconfile)
          
    def quit(self):
        if self.okayToQuit():
            if askyesno(self.__app, "Verify Quit Program?"):
                self.destroy()
            else:
                showinfo(self.__app, "Quit not allowed")
                
    def destroy(self):
        Tk.quit(self)
        
    def okayToQuit(self):
        return True
    
class PopupWindow(Toplevel, _window):
    def __init__(self, app, kind="", iconfile=None):
        Toplevel.__init__(self)
        self.__app = app
        self.configBorders(app, kind, iconfile)
        
    def quit(self):
        if askyesno(self.__app, "Verify Quit Window?"):
            self.destroy()
            
    def destroy(self):
        Toplevel.destroy(self)