from SharedNames import *

class PyArmCalcCommon():
    threadLoopStarted = False
    queueCheckPerSecond = 10
    queueDelay = 1000 // queueCheckPerSecond
    queueBatch = 5

    def __init__(self):
        self.makeWidgets()
        self.armDict = self.makeArmDict()
        
        if not PyArmCalcCommon.threadLoopStarted:
            PyArmCalcCommon.threadLoopStarted = True
            threadtools.threadChecker(self, self.queueDelay, self.queueBatch)
                        
    def makeWidgets(self):
        # add main fields at top
        field = Frame(self, relief=SUNKEN, bd=2, cursor="hand2")
        field.pack(side=TOP, fill=X)
        var1 = self.make_row(field, label="Diametr", label_width=10, width=10)
        var2 = self.make_row(field, label="Length", label_width=10, width=10)
        var3 = self.make_row(field, label="Amount", label_width=10, width=10)
        count = lambda: self.onCount(var1.get(), var2.get(), var3.get())
        Button(field, text="count", command=count).pack(side=RIGHT)
        
        # add tools at bottom
        tools = Frame(self, relief=SUNKEN, bd=2, cursor="hand2")
        tools.pack(side=BOTTOM, fill=X)
        Button(tools, text="Load data", command=self.onLoadData).pack(side=LEFT)
        Button(tools, text="Clear all", command=self.onClearAll).pack(side=RIGHT)
        Button(tools, text="Count all", command=self.onCountAll).pack(side=RIGHT)
        Button(tools, text="Delete", command=self.onDelete).pack(side=RIGHT)
        
        # add listbox with scrollbar
        listwide = 70
        listheigh = 15
        mainfield = Frame(self)
        vscroll = Scrollbar(mainfield)
        fontsz = (sys.platform[:3] == 'win' and 10) or 10
        listbg = "white"
        listfg = "black"
        listfont = ("courier", fontsz, "normal")
        listbox = Listbox(mainfield, bg=listbg, fg=listfg, font=listfont)
        listbox.config(selectmode=EXTENDED)
        listbox.config(width=listwide, height=listheigh)
        
        vscroll.config(command=listbox.yview, relief=SUNKEN)
        listbox.config(yscrollcommand=vscroll.set, relief=SUNKEN)
        
        mainfield.pack(expand=YES, fill=BOTH)
        vscroll.pack(side=RIGHT, fill=BOTH)
        listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.listbox = listbox
        
        self.pasteString(headers)
        
    def makeArmDict(self):
        d1 = {i: [str(i), "-", "-", "-", "0"] for i in range(3, 9, 1)}
        d2 = {i: [str(i), "-", "-", "-", "0"] for i in range(10, 24, 2)}
        armDict = {25: ["25", "-", "-", "-", "0"]}
        d3 = {i: [str(i), "-", "-", "-", "0"] for i in range(28, 44, 4)}
        for i in (d1, d2, d3):
            armDict.update(i)
        return armDict
        
    def make_row(self, parent, label, label_width=20, width=20):
        var = StringVar()
        row = Frame(parent)
        lab = Label(row, text=label, relief=RIDGE, width=label_width)
        ent = Entry(row, relief=SUNKEN, textvariable=var, width=width)
        row.pack(side=LEFT)
        lab.pack(side=LEFT)
        ent.pack(side=LEFT)
        return var

    def pasteString(self, items):
        line = ""
        for i in items:
            gap = 12 - len(i)
            line += " " + i + " " * gap + "|"
        self.listbox.insert(END, line[:-1])
        self.listbox.see(END)
        
    def CountAll(self, list_items):
        for i in list_items:
            self.onCount(*i)
        
    def onCount(self, d, l, a):
        items = []
        items.append(d)
        items.append(l)
        items.append(a)
        #w_1 = 3.14 * pow(int(d), 2) / 4000000 * 7850 * int(l) / 1000
        w_1 = armWeight[d] * int(l) / 1000
        items.append("%.2f" % w_1)
        items.append("%.2f" % (w_1 * int(a)))
        self.armDict[int(d)][4] = "%.2f" % (float(self.armDict[int(d)][4]) + w_1 * int(a))
        self.pasteString(items)
        
    def onDelete(self):
        index = self.listbox.curselection()
        for i in index:
            string = self.listbox.get(i)
            string.strip()
            sl = string.split()
            d, w = sl[0], sl[-1]
            self.armDict[int(d)][4] = "%.2f" % (float(self.armDict[int(d)][4]) - float(w))
        try:
            for i in index[::-1]:
                self.listbox.delete(i)
        except: pass
        
    def onClearAll(self):
        self.listbox.delete(0, END)
        self.pasteString(headers)
        
    def onCountAll(self):
        line = ""
        for i in range(5):
            gap = 13
            line += "-" * gap + "|"
        self.listbox.insert(END, line[:-1])
        for i in self.armDict.keys():
            if self.armDict[i][4] not in ["0", "0.0", "0.00"]:
                self.pasteString(self.armDict[i])
        self.listbox.insert(END, line[:-1])
        self.armDict = self.makeArmDict()
        
    def onLoadData(self): ViewWindow()

class ViewWindow(windows.PopupWindow):
    def __init__(self):
        self.width = viewwindow_width
        windows.PopupWindow.__init__(self, appname, "Load data")
        self.makeWidgets()
        
    def makeWidgets(self):
        # add canvas with scrollbar
        mainfield = Frame(self)
        mainfield.pack(expand=YES, fill=BOTH)
                
        vbar = Scrollbar(mainfield)
        hbar = Scrollbar(mainfield, orient="horizontal")
        vbar.pack(side=RIGHT, fill=Y)
        hbar.pack(side=BOTTOM, fill=X)
               
        canvas = Canvas(mainfield)
        canvas.config(borderwidth=0)
        canvas.pack(side=TOP, fill=BOTH, expand=YES)
        
        vbar.config(command=canvas.yview)
        hbar.config(command=canvas.xview)
        canvas.config(yscrollcommand=vbar.set)
        canvas.config(xscrollcommand=hbar.set)
                        
        self.canvas = canvas
        
        # add tools at bottom
        tools = Frame(self, relief=SUNKEN, bd=2, cursor="hand2")
        tools.pack(side=BOTTOM, fill=X)
        Button(tools, text="Recognize", command=self.onRecognizeData).pack(side=RIGHT, fill=X)
        Button(tools, text="Open", command=self.onOpen).pack(side=LEFT, fill=X)
        
    def onOpen(self):
        try:
            imgpath = openDialog.show()
        except: pass
        if imgpath:
            self.imgpath = imgpath
            self.title(appname + " " + imgpath)
            
            imgpil = Image.open(imgpath)
            imgwide, imghigh = imgpil.size
            scale = imgwide // self.width
            newwide, newhigh = imgwide // scale, imghigh // scale
            imgpil = imgpil.resize((newwide, newhigh), Image.BICUBIC)
            self.imgtk = imgtk = PhotoImage(image=imgpil)   # prevent to be garbage collected
                    
            canvas = self.canvas
            canvas.delete("all")
            canvas.config(height=newhigh, width=newwide)
            canvas.config(scrollregion=(0, 0, newwide, newwide))
            canvas.create_image(0, 0, image=imgtk, anchor=NW)
            self.lift()
                        
    def onRecognizeData(self):
        try:
            imgpath = self.imgpath
        except: pass
        if imgpath:
            threadtools.startThread(
                action=self.Recognise,
                args=(imgpath,),
            )
        
    def Recognise(self, imgpath):
        id = str(uuid.uuid4())
        temp_dir = os.getcwd() + '\\temp_words\\' + id + "\\"
        test_image = self.imgpath
        lines_list, words_dir = KerasTextRecog.ProcessText(test_image, temp_dir).image_to_words()
        predictions_list = []
        for line in lines_list:
            for item in line:
                digits_list, word_dir = KerasTextRecog.ProcessWord(item, words_dir).image_to_digits()
                predictions = KerasTextRecog.ProcessDigitsList(word_dir).list_to_digits()
                predictions_list.append(predictions)
        shutil.rmtree(temp_dir)    
        lines_list = []
        for i in range(0, len(predictions_list), 3):
            lines_list.append(predictions_list[i : i+3])
        for line in lines_list:
            yield PyArmCalcCommon.onCount, (self.master, *line)