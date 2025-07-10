""" 
#######################################################################
PyArmCalc 1.0 - a Python/tkinter arm calc.
A tkinter-based GUI interface for engeneering calculations. Previously
for reinforcing bars calculation with another functions in future.

This file implements the top-level windows and interface.

==Modules used here==

here is a list that will be expanced
"""

from SharedNames import windows, appname, iconfile
from ListWindows import PyArmCalcCommon

class ArmCalcWindow(PyArmCalcCommon, windows.MainWindow):
    def __init__(self):
        windows.MainWindow.__init__(self, appname, iconfile=iconfile)
        PyArmCalcCommon.__init__(self)
    

############################################################
# when run as a top-level program: create main calc window
############################################################

if __name__ == "__main__":
    rootwin = ArmCalcWindow()
    rootwin.mainloop()