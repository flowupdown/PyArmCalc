appname = "PyArmCalc 1.0"
headers = ["Diametr", "Length", "Amount", "Weigth one", "Weigth all"]
viewwindow_width = 500
model = "mnist_dataset.keras"
iconfile = "d:\\programming\\python\\PyArmCalc\\iron-bar.png"
diam = [str(i) for i in [6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40]]
weight = [i for i in [0.222, 0.395, 0.617, 0.888, 1.208, 1.578, 1.998, 2.466,
                      2.984, 3.853, 4.834, 6.313, 7.99, 9.865]]
armWeight = {k: v for k, v in zip(diam, weight)}

from tkinter import *
import windows
import threadtools
import sys
from tkinter.filedialog import SaveAs, Open, Directory
from PIL import Image
from PIL.ImageTk import PhotoImage
import KerasTextRecog
import uuid
import os
import shutil

openDialog = Open(title=appname + ": Open File")
saveDialog = SaveAs(title=appname + ": Save File")