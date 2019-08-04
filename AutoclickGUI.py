import keyboard, wx, os, threading
from time import sleep, time
from random import randint


class PlaceholderTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        self.default_text = kwargs.pop("placeholder", "")
        wx.TextCtrl.__init__(self, *args, **kwargs)
        self.OnKillFocus(None)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

    def OnFocus(self, evt):
        self.SetForegroundColour(wx.BLACK)
        if self.GetValue() == self.default_text:
            self.SetValue("")
        evt.Skip()

    def OnKillFocus(self, evt):
        if self.GetValue().strip() == "":
            self.SetValue(self.default_text)
            self.SetForegroundColour(wx.LIGHT_GREY)
        if evt:
            evt.Skip()

class AutoMacroEditor(wx.Frame):
    def __init__(self, parent, title, main, edit = None):
        wx.Frame.__init__(self, parent, title = title, size = (400,250), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.main = main
        self.panel = wx.Panel(self, size = (200,250), style = wx.SUNKEN_BORDER)

        self.namelab = wx.StaticText(self.panel, label = "Macro Name: ", size = (100,20), pos = (10,10), style = wx.TE_MULTILINE)
        self.Macrolab = wx.StaticText(self.panel, label = "Activation Key: ", size = (100,20), pos = (10,40), style = wx.TE_MULTILINE)
        self.Hotkeylab = wx.StaticText(self.panel, label = "Button to press: ", size = (100,20), pos = (10,70), style = wx.TE_MULTILINE)
        self.Timelab = wx.StaticText(self.panel, label = "Repeat Time secs: ", size = (100,20), pos = (10,100), style = wx.TE_MULTILINE)

        self.Macrobut = wx.Button(self.panel, label = "Set Key", pos = (225,40), size = (125, 25))
        self.Hotkeybut = wx.Button(self.panel, label = "Set Key", pos = (225,70), size = (125, 25))
        self.CreateKey = wx.Button(self.panel, label = "CREATE AUTO-MACRO THING", pos = (100,140), size = (175, 50))
        self.Bind(wx.EVT_BUTTON, self.get_mkey, self.Macrobut)
        self.Bind(wx.EVT_BUTTON, self.get_hkey, self.Hotkeybut)

        if edit != None:
            self.origname = edit
            self.MacroName = wx.TextCtrl(self.panel, value = edit, pos = (125,10), size = (150,20))
            self.MacroKey = wx.TextCtrl(self.panel, value = main.entryvals[edit][0], size = (100,20), pos = (125,40), style = wx.TE_READONLY)
            self.HotKeyKey = wx.TextCtrl(self.panel, value = main.entryvals[edit][1], size = (100,20), pos = (125,70), style = wx.TE_READONLY)
            self.TimeDelay = wx.TextCtrl(self.panel, value = str(main.entryvals[edit][4]), size = (100,20), pos = (125,100))
            self.Bind(wx.EVT_BUTTON, self.edit, self.CreateKey)

        else:
            self.MacroName = PlaceholderTextCtrl(self.panel, value = "Macro Name", pos = (125,10), size = (150,20), placeholder = "Macro Name")
            self.MacroKey = wx.TextCtrl(self.panel, value = "", size = (100,20), pos = (125,40), style = wx.TE_READONLY)
            self.HotKeyKey = wx.TextCtrl(self.panel, value = "", size = (100,20), pos = (125,70), style = wx.TE_READONLY)
            self.TimeDelay = wx.TextCtrl(self.panel, value = str(10), size = (100,20), pos = (125,100))
            self.Bind(wx.EVT_BUTTON, self.add, self.CreateKey)



    def add(self, event):
        MacName = self.MacroName.GetValue()
        MacKey = self.MacroKey.GetValue()
        HKK = self.HotKeyKey.GetValue()
        TD = int(self.TimeDelay.GetValue())
        if not(MacName != "" or MacName[0] != " "):
            print("Eff off mate")
            return
        if not(MacKey != ""):
            print("OI!")
            return
        if not(HKK != ""):
            print("ENough")
            return
        try:
            abs(int(TD))
        except:
            print("NOOO")
            return
        self.main.entries.append(MacName)
        self.main.entryvals[MacName] = [MacKey, HKK, False, False, TD, time()]
        self.main.entrylist.InsertItems([MacName],len(self.main.entries)-1)
        self.main.entrylist.SetItemBackgroundColour(len(self.main.entries)-1, wx.RED)
        self.contentNotSaved = True
        self.Destroy()

    def edit(self, event):
        MacName = self.MacroName.GetValue()
        MacKey = self.MacroKey.GetValue()
        HKK = self.HotKeyKey.GetValue()
        TD = int(self.TimeDelay.GetValue())
        if not(MacName != "" or MacName[0] != " "):
            print("Eff off mate")
            return
        if not(MacKey != ""):
            print("OI!")
            return
        if not(HKK != ""):
            print("ENough")
            return
        try:
            abs(int(TD))
        except:
            print("NOOO")
            return
        self.main.entrylist.Delete(self.main.entries.index(self.origname))
        del self.main.entryvals[self.origname]
        self.main.entries.remove(self.origname)
        self.main.entries.append(MacName)
        self.main.entryvals[MacName] = [MacKey, HKK, False, False, TD, time()]
        self.main.entrylist.InsertItems([MacName],len(self.main.entries)-1)
        self.main.entrylist.SetItemBackgroundColour(len(self.main.entries)-1, wx.RED)
        self.contentNotSaved = True
        self.Destroy()


    def get_mkey(self, event):
        mkey = ""
        mkey = keyboard.read_hotkey(False)
        self.MacroKey.SetValue(mkey)

    def get_hkey(self, event):
        hkey = ""
        hkey = keyboard.read_hotkey(False)
        self.HotKeyKey.SetValue(hkey)

class MainWindow(wx.Frame):
    def __init__(self,parent,title):
        self.contentNotSaved = False
        #set entryvals as "Hotkey Name" ("Activator hotkey", "Thing to click", toggleval, listenval, time wait, lasttime pressed)
        self.entryvals = {}
        self.entries = []
        self.Profile = None
        self.Default = None

        wx.Frame.__init__(self,parent,title=title, size=(400,211))
        tmp = wx.LogNull()

        panel = wx.Panel(self, size = (400,200), style = wx.SUNKEN_BORDER)
        box = wx.BoxSizer(wx.HORIZONTAL)
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)

        self.text = wx.StaticText(panel, label =" Item 1: \n Item 2:  \n HotKey active:  \n Listening: \n Type: ", size = (100,75),style = wx.TE_MULTILINE)

        self.entrylist = wx.ListBox(panel, size = (100, 100), choices = self.entries, style = wx.LB_SINGLE | wx.LB_OWNERDRAW)

        self.creationwinbut = wx.Button(panel, label = "Create Macro", pos = (150,-200), size = (125, 25))
        self.Bind(wx.EVT_BUTTON, self.createcreationwin, self.creationwinbut)
        self.creationwinbut.Show(True)

        self.editwinbut = wx.Button(panel, label = "Edit Macro", pos = (150,-175), size = (125,25))
        self.Bind(wx.EVT_BUTTON, self.editwin, self.editwinbut)


        leftbox.Add(self.entrylist, 0, wx.EXPAND)
        leftbox.Add(self.creationwinbut, 0, wx.EXPAND)
        rightbox.Add(self.text, 1, wx.EXPAND)
        rightbox.Add(self.editwinbut, 0, wx.EXPAND)

        box.Add(leftbox, 0, wx.EXPAND)
        box.Add(rightbox, 0, wx.EXPAND)


        panel.SetSizer(box)
        panel.Fit()
        self.Bind(wx.EVT_LISTBOX, self.OnMacroList, self.entrylist)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.toggleListenHotkey, self.entrylist)


        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Double Click to Activate Listening for hotkey')

        filemenu=wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About","Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open saved Profile")
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        menuSave = filemenu.Append(wx.ID_SAVE, "&Save As", "Save current profile")
        self.Bind(wx.EVT_MENU, self.OnSaveProfAs, menuSave)

        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        self.DefProfileMenu = wx.Menu()
        self.Profiles = os.listdir(os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\\\")+"\\Profiles\\")
        self.profilemenus = []
        self.Profiles.remove("Default_Profile.BradBotDef")

        with open(str(os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\\\"))+"\\Profiles\\Default_Profile.BradBotDef", 'r') as Default:
            Defaultprof = Default.readline()
        if Defaultprof != "None":
            try:
                with open(Defaultprof, 'r') as file:
                    self.doLoadData(file, Defaultprof)
            except:
                print("No Default")
        else:
            print("No Default")


        for x in self.Profiles:
            self.profilemenus.append(self.DefProfileMenu.Append(wx.ID_ANY, x, "Profile", kind=wx.ITEM_CHECK))
            self.Bind(wx.EVT_MENU, self.Flip, self.profilemenus[-1])
            if str(os.path.dirname(os.path.realpath(__file__)) + "\\Profiles\\" + x) == Defaultprof:
                self.profilemenus[-1].Check()
                self.Default = self.profilemenus[-1].GetId()

        menubar = wx.MenuBar()
        menubar.Append(filemenu,"&File")
        menubar.Append(self.DefProfileMenu, "&Default Profile")
        self.SetMenuBar(menubar)
        self.Show(True)

        if wx.Icon("Assets/YTLogoBaseMKI.ico").IsOk():
            self.SetIcon(wx.Icon("Assets/YTLogoBaseMKI.ico"))
        else:
            self.MissingIcon()

        self.listenthread = threading.Thread(target = self.timedhotkey)
        self.listenthread.start()



    def Flip(self, event):
        print(self.Default)
        for x in self.profilemenus:
            if x.GetId() != self.Default and x.IsChecked():
                if self.Default != None:
                    print(self.Default)
                    self.DefProfileMenu.Check(self.Default,False)
                self.Default = x.GetId()
                print("Wah")
            elif x.GetId() == self.Default and not x.IsChecked():
                print("test")
                self.Default = None
        if self.Default != None:
            with open(str(os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\"))+"\\Profiles\\Default_Profile.BradBotDef", 'w') as Default:
                Default.write(str(os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\"))+"\\Profiles\\" + self.DefProfileMenu.GetLabel(self.Default))
        else:
            with open(str(os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\"))+"\\Profiles\\Default_Profile.BradBotDef", 'w') as Default:
                Default.write("None")

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "A small macro clicker thing", "An auto clicker with variable macros and timings")
        dlg.ShowModal()
        dlg.Destroy()

    def OnOpen(self, event):
        if self.contentNotSaved:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open XYZ file", wildcard="BradBot files (*.BradBot)|*.BradBot", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            fileDialog.SetDirectory(str(os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\\\"))+"\\Profiles\\")

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.doLoadData(file, pathname)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

    def doLoadData(self, file, pathname):
        self.Profile = pathname.split("\\")[-1].split(".")[0]
        entryline = file.readline()
        for name in self.entries:
            self.entrylist.Delete(self.entries.index(name))

        self.entries = entryline.split(", ")[:-1]
        for pos in range(0, len(self.entries)):
            self.entrylist.InsertItems([self.entries[pos]],pos)
            self.entrylist.SetItemBackgroundColour(pos, wx.RED)
        for entrypos in range(0, len(self.entries)):
            newentry = file.readline().split(", ")[:-1]
            newentry.append(time())
            newentry[4] = int(newentry[4])
            self.entryvals[self.entries[entrypos]] = newentry

    def OnSaveProfAs(self, event):
        workdi = str(os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\\\"))+"\\Profiles\\"
        with wx.FileDialog(self, "Save Profile", wildcard="BradBot File (*.BradBot)|*.BradBot", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            fileDialog.SetDirectory(workdi)

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.doSaveData(file,pathname)
                self.contentNotSaved = False
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def doSaveData(self, file, pathname):
        self.Profile = pathname.split("\\")[-1].split(".")[0]
        for entry in self.entries:
            file.write("{}, ".format(entry))
        for entry in self.entries:
            file.write("\n")
            for data in self.entryvals[entry][:-1]:
                file.write("{}, ".format(data))

    def MissingFile(self, FType):
        dlg = wx.MessageDialog(self, "Missing File", "Missing {} in {}".format(FType[0], FType[1]))
        dlg.ShowModal()
        dlg.Destroy()

    def MissingIcon(self):
        dlg = wx.MessageDialog(self, "Missing File", "Missing Icon File in Assets File")
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self,event):
        try:
            self.creationwindow.Destroy()
        except:
            pass
        self.Destroy()
        os._exit(0)


    def OnMacroList(self, event):
        try:
            entry=event.GetEventObject().GetStringSelection()
        except:
            entry=event
        self.text.SetLabel(" Item 1: {}, \n Item 2: {} \n HotKey active: {} \n Listening: {}\n Type: ".format(self.entryvals[entry][0],self.entryvals[entry][1],self.entryvals[entry][2],self.entryvals[entry][3]))

    def toggleListenHotkey(self, event):
        entry=event.GetEventObject().GetStringSelection()
        self.entryvals[entry][3] = not self.entryvals[entry][3]
        if self.entryvals[entry][3]:
            self.entrylist.SetItemBackgroundColour(self.entrylist.GetSelection(), wx.GREEN)
        else:
            self.entrylist.SetItemBackgroundColour(self.entrylist.GetSelection(), wx.RED)
        self.OnMacroList(event)
        if not (self.listenthread.is_alive()):
            self.listenthread = threading.Thread(target = self.timedhotkey)
            self.listenthread.start()


    def createcreationwin(self, event):
        self.creationwindow = AutoMacroEditor(None, "Macro Editor", self)
        self.creationwindow.Show()

    def editwin(self, event):
        try:
            currselect = self.entrylist.GetString(self.entrylist.GetSelection())
            self.creationwindow = AutoMacroEditor(None, "Macro Editor", self, currselect)
            self.creationwindow.Show()
        except:
            print("How tf")

    def timedhotkey(self):
        diff = 0
        run = True
        for Hotkey in self.entries:
            #print(Hotkey)
            self.entryvals[Hotkey][5] = time()

        while(run):
            run = False
            for Hotkey in self.entries:
                currhotkey = self.entryvals[Hotkey][0]
                if self.entryvals[Hotkey][3]:
                    run = True
                if keyboard.is_pressed(currhotkey) and self.entryvals[Hotkey][3]:
                    self.entryvals[Hotkey][2] = not self.entryvals[Hotkey][2]
                    self.OnMacroList(Hotkey)
                    sleep(0.2)
                if self.entryvals[Hotkey][2]:
                    currtime=time()
                    diff = abs(int(self.entryvals[Hotkey][5] - currtime))
                    if diff >= self.entryvals[Hotkey][4]:
                        diff = 0
                        self.entryvals[Hotkey][5] = currtime
                        keyboard.press(self.entryvals[Hotkey][1])
                        sleep(0.05)
                        keyboard.release(self.entryvals[Hotkey][1])





app = wx.App(False)
frame = MainWindow(None, "BradBot Auto-Clicker So im always here")

app.MainLoop()
