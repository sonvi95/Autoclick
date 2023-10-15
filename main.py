import re
import threading
import time

import wx
import mouse
import keyboard

class LeftPanel(wx.Panel):
    def __init__(self,parent):
        self.parent = parent
        wx.Panel.__init__(self,parent)
        # self.SetBackgroundColour(wx.BLUE)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        #coordinate
        coor_stt = wx.StaticText(self,label="Coordinate")
        left_sizer.Add(coor_stt,0,wx.EXPAND|wx.ALL,10)

        #xy
        xy_sizer = wx.BoxSizer(wx.HORIZONTAL)
        x_sts = wx.StaticText(self,label="x: ")
        self.x_txt = wx.TextCtrl(self,size=(50,-1),style = wx.TE_READONLY)
        y_sts = wx.StaticText(self, label="y: ")
        self.y_txt = wx.TextCtrl(self,size=(50,-1),style = wx.TE_READONLY)

        xy_sizer.Add(x_sts,0,wx.ALL,5)
        xy_sizer.Add(self.x_txt, 1, wx.ALL, 5)
        xy_sizer.Add(y_sts, 0, wx.ALL, 5)
        xy_sizer.Add(self.y_txt, 1, wx.ALL, 5)

        left_sizer.Add(xy_sizer, 0, wx.EXPAND | wx.ALL, 10)

        #Time Setting
        time_stt = wx.StaticText(self,label="Time Setting")
        left_sizer.Add(time_stt,0,wx.EXPAND|wx.ALL,10)

        fgs = wx.FlexGridSizer(5, 3, 10, 10)
        #click interval
        inter_stt = wx.StaticText(self,label="Click Interval")
        self.inter_txt = wx.TextCtrl(self)
        self.inter_txt.Bind(wx.EVT_KEY_DOWN,self.UpdateText)
        inter_unit = wx.StaticText(self,label = "ms")

        #stop after
        stop_stt = wx.StaticText(self,label="Stop After")
        self.stop_txt = wx.TextCtrl(self,style = wx.TE_READONLY)
        self.stop_txt.Bind(wx.EVT_KEY_DOWN, self.UpdateText)
        stop_unit = wx.StaticText(self,label = "Clicks")

        #current
        curclick_stt = wx.StaticText(self,label="Current")
        self.curclick_txt = wx.TextCtrl(self,style = wx.TE_READONLY)
        self.curclick_txt.Bind(wx.EVT_KEY_DOWN, self.UpdateText)
        curclick_unit = wx.StaticText(self,label = "Clicks")

        #stop after
        stoptime_stt = wx.StaticText(self,label="Stop After")
        self.stoptime_txt = wx.TextCtrl(self,style = wx.TE_READONLY)
        self.stoptime_txt.Bind(wx.EVT_KEY_DOWN, self.UpdateText)
        stoptime_unit = wx.StaticText(self,label = "mins")

        #current
        curtime_stt = wx.StaticText(self,label="Current")
        self.curtime_txt = wx.TextCtrl(self,style = wx.TE_READONLY)
        self.curtime_txt.Bind(wx.EVT_KEY_DOWN, self.UpdateText)
        curtime_unit = wx.StaticText(self,label = "")

        fgs.AddMany([(inter_stt), (self.inter_txt, 1, wx.EXPAND),(inter_unit),
                     (stop_stt), (self.stop_txt, 1, wx.EXPAND),(stop_unit),
                     (curclick_stt),(self.curclick_txt, 1, wx.EXPAND), (curclick_unit),
                     (stoptime_stt),(self.stoptime_txt, 1, wx.EXPAND),(stoptime_unit),
                     (curtime_stt),(self.curtime_txt, 1, wx.EXPAND),(curtime_unit),])
        left_sizer.Add(fgs, 0, wx.EXPAND | wx.ALL, 10)

        #Select button
        select_stt = wx.StaticText(self,label="Select Button")
        left_sizer.Add(select_stt,0,wx.EXPAND|wx.ALL,10)

        radio_sizer = wx.BoxSizer(wx.HORIZONTAL)
        radio_left = wx.RadioButton(self,label="Left",style=wx.RB_GROUP)
        radio_right = wx.RadioButton(self, label="Right")
        radio_sizer.Add(radio_left,0,wx.ALL|wx.EXPAND,10)
        radio_sizer.Add(radio_right, 0, wx.ALL | wx.EXPAND, 10)
        left_sizer.Add(radio_sizer, 0, wx.CENTRE | wx.ALL, 0)

        checkbox = wx.CheckBox(self, -1, "Window always on Top")
        checkbox.SetValue(True)
        checkbox.Bind(wx.EVT_CHECKBOX,self.SetWinTop,checkbox)
        left_sizer.Add(checkbox, 0, wx.CENTER | wx.ALL, 0)

        self.SetSizer(left_sizer)
        self.SetValue()

    def SetWinTop(self,evt):
        obj = evt.GetEventObject().GetValue()
        if obj:
            self.parent.SetWindowStyle(wx.STAY_ON_TOP)
        else:
            self.parent.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)

    def SetValue(self):
        self.inter_txt.SetValue('600')
        self.stop_txt.SetValue('10')
        self.curclick_txt.SetValue('0')
        self.stoptime_txt.SetValue('0')
        self.curtime_txt.SetValue('0')

    def UpdateText(self,evt):
        if evt.GetKeyCode()>=48 and evt.GetKeyCode()<=57:
            print(evt.GetKeyCode())
            evt.Skip()
        elif evt.GetKeyCode() == wx.WXK_BACK:
            evt.Skip()

    def SetXY(self,x,y):
        self.x_txt.SetValue(str(x))
        self.y_txt.SetValue(str(y))

    def GetData(self):
        inter = self.inter_txt.GetValue()
        stop = self.stop_txt.GetValue()
        curclick = self.curclick_txt.GetValue()
        stoptime = self.stoptime_txt.GetValue()
        curtime = self.curtime_txt.GetValue()
        return {'inter':int(inter),'stop':int(stop)}

class RightPanel(wx.Panel):
    def __init__(self,parent):
        self.parent = parent
        wx.Panel.__init__(self,parent)
        # self.SetBackgroundColour(wx.YELLOW)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        #X-Y list
        xylist_stt = wx.StaticText(self,label="X-Y list")
        right_sizer.Add(xylist_stt,0,wx.EXPAND|wx.ALL,10)

        #main text
        self.maintext= wx.TextCtrl(self,style = wx.TE_MULTILINE )
        right_sizer.Add(self.maintext, 1, wx.EXPAND | wx.ALL, 10)

        #count
        cnt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        cnt_stt = wx.StaticText(self,label="Count")
        self.cnt_txt = wx.TextCtrl(self,style = wx.TE_READONLY)
        cnt_sizer.Add(cnt_stt,0,wx.ALL|wx.EXPAND,5)
        cnt_sizer.Add(self.cnt_txt, 0, wx.ALL | wx.EXPAND, 5)
        right_sizer.Add(cnt_sizer, 0, wx.EXPAND | wx.ALL, 0)

        #button
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_btn = wx.Button(self,label='Save')
        save_btn.Bind(wx.EVT_BUTTON,self.SaveFile)
        load_btn = wx.Button(self,label='Load')
        load_btn.Bind(wx.EVT_BUTTON, self.LoadData)
        btn_sizer.Add(save_btn,1,wx.ALL|wx.CENTER,10)
        btn_sizer.Add(load_btn, 1, wx.ALL | wx.CENTER, 10)
        right_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 0)

        #description
        des_stt = wx.StaticText(self,label= "\n   [SPACE] : Set poin\n   [ESC] : Stop\n   [PAUSE] : Pause\n   [DEL] : Clear list\n")
        des_stt.SetBackgroundColour(wx.YELLOW)
        right_sizer.Add(des_stt, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(right_sizer)

#         self.maintext.SetValue('''x: 277 y: 369
# x: 277 y: 369
# x: 282 y: 185
# x: 282 y: 185
# x: 179 y: 109
# x: 179 y: 109
# x: 131 y: 343
# x: 131 y: 343
# ''')
        self.cnt_txt.SetValue('0')

    def SaveFile(self,evt):
        fdlg = wx.FileDialog(self, "Input setting file path", wildcard="config files(*.config)|*.config", style=wx.FD_SAVE)

        if fdlg.ShowModal() == wx.ID_OK:
            print(fdlg.GetPath())
            f = open(fdlg.GetPath(), "w+")
            f.write(self.maintext.GetValue())
            f.close()

    def LoadData(self,evt):
        load_thead = threading.Thread(target=self.parent.StartRecode)
        load_thead.start()

    def UpdateData(self,mouse_events):
        save_x = 0
        save_y = 0
        data_save = ''
        idx = 0
        for evt in mouse_events:
            # print(type(evt))
            if type(evt) is mouse._mouse_event.MoveEvent:
                # print('x: ', evt.x, ' y: ', evt.y)
                save_x = evt.x
                save_y = evt.y

            elif type(evt) is mouse._mouse_event.ButtonEvent:
                if evt.event_type == 'up' and evt.button == 'left':
                    data_save+='x: '+str(save_x)+'      y: '+str(save_y)+'\n'
                    idx+=1
        print(data_save)
        self.cnt_txt.SetValue(str(idx))
        self.maintext.SetValue(data_save)

    def GetData(self):
        data = self.maintext.GetValue()
        list_data = re.split('\n',data)
        list_return = []
        for line in list_data:
            mathdata = re.match('x:\s+([0-9-]+)\s+y:\s+([0-9-]+)',line)
            if mathdata:
                list_return.append({'x':int(mathdata.groups()[0]),'y':int(mathdata.groups()[1])})
        return list_return

class MainFrame(wx.Frame):
    def __init__(self,parent):

        self.running = 0

        wx.Frame.__init__(self,parent,title='Auto Click')
        self.SetSize(500,600)

        #####################
        menubar = wx.MenuBar()

        save_menu = wx.Menu()
        menubar.Append(save_menu,'File')

        newitem = wx.MenuItem(save_menu, wx.ID_NEW, text="Open")
        save_menu.Append(newitem)


        self.SetMenuBar(menubar)

        #####################

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.leftpanel = LeftPanel(self)
        self.rightpanel = RightPanel(self)

        top_sizer.Add(self.leftpanel,1,wx.ALL|wx.EXPAND,0)
        top_sizer.Add(self.rightpanel, 1, wx.ALL | wx.EXPAND, 0)
        main_sizer.Add(top_sizer,1,wx.ALL|wx.EXPAND,0)

        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        start_btn = wx.Button(self,label='Start')
        start_btn.Bind(wx.EVT_BUTTON,self.RunRecord)
        cancel_btn = wx.Button(self,label='Cancel')
        cancel_btn.Bind(wx.EVT_BUTTON,self.StopRunning)
        bottom_sizer.Add(start_btn,1,wx.ALL|wx.CENTER,10)
        bottom_sizer.Add(cancel_btn, 1, wx.ALL | wx.CENTER, 10)
        main_sizer.Add(bottom_sizer, 0, wx.ALL | wx.CENTER , 0)

        self.SetSizer(main_sizer)


        self.Show()

        self.mouse_events = []

        self.app_running = 1

        self.Bind(wx.EVT_CLOSE,self.CloseFrame)
        self.Bind(wx.EVT_MENU,self.OpenFile)

        boad_thead = threading.Thread(target=self.CheckPress)
        boad_thead.start()

        mouse_thead = threading.Thread(target=self.CheckMouse)
        mouse_thead.start()
        self.SetWindowStyle(wx.STAY_ON_TOP)

    def OpenFile(self,event):
        dlg = wx.FileDialog(self, "OPEN EMG FILE", wildcard="TXT Files(*.config)|*.config",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            f = open(dlg.GetPath(), "r")
            self.rightpanel.maintext.SetValue(f.read())
            f.close()

    def StopRunning(self,evt):
        self.running = 0

    def CloseFrame(self,evt):
        self.app_running = 0
        self.running = 0
        evt.Skip()

    def CheckMouse(self):
        while True:
            # print(mouse.get_position())
            pos = mouse.get_position()
            self.leftpanel.SetXY(pos[0],pos[1])
            time.sleep(0.01)

            if self.app_running == 0:
                break

    def CheckPress(self):
        val = ''
        while True:
            tem = keyboard.get_hotkey_name()
            if tem == '':
                val = ''
                time.sleep(0.05)
            else:
                if val == '':
                    val = tem
                    print('val: ',val)
                    if val == 'esc':
                        self.running = 0
                    elif val == 'space':
                        pos = mouse.get_position()
                        data_tem = self.rightpanel.maintext.GetValue().strip() + '\nx: '+str(pos[0])+'      y: '+str(pos[1])
                        print(data_tem.encode())
                        self.rightpanel.maintext.SetValue(data_tem.strip())
                        self.rightpanel.cnt_txt.SetValue(str(int(self.rightpanel.cnt_txt.GetValue())+1))
                    elif val == 'delete':
                        self.rightpanel.maintext.SetValue('')
                        self.rightpanel.cnt_txt.SetValue('0')
                    elif val == 'pause':
                        if self.running == 1:
                            self.running = 2
                    time.sleep(0.05)
                else:
                    time.sleep(0.1)

            if self.app_running == 0:
                break

    def StartRecode(self):
        print('StartRecode')
        self.running = 1
        mouse.hook(self.mouse_events.append)
        while self.running != 0:
            time.sleep(0.01)
        mouse.unhook(self.mouse_events.append)
        print(self.mouse_events)
        self.rightpanel.UpdateData(self.mouse_events)
        self.mouse_events = []
        self.running = 0

    def RunRecord(self,evt):
        print(self.running)
        if self.running == 2:
            self.running=1
        else:
            m_thread = threading.Thread(target=self.ReplayAction)
            m_thread.start()



    def ReplayAction(self):
        data_setup = self.leftpanel.GetData()
        data_record = self.rightpanel.GetData()
        mouse_evt = []
        time_idx = 1
        for data in data_record:
            mouse_evt.append(mouse.MoveEvent(data['x'],data['y'],time_idx))
            time_idx+=data_setup['inter']/1000
        self.running = 1
        l_max = data_setup['stop']
        l_click = len(data_record)
        for number in range(0, data_setup['stop']):
            d = l_max - number-1
            for idx,data in enumerate(data_record):
                while self.running == 2:
                    time.sleep(0.1)

                if self.running == 0:
                    return

                v = l_click - idx -1
                val = (d*l_click+v)*data_setup['inter']
                self.leftpanel.stoptime_txt.SetValue(str(val))

                mouse.move(data['x'],data['y'])
                mouse.click('left')
                time.sleep(data_setup['inter']/1000)

            self.leftpanel.curclick_txt.SetValue(str(number+1))


app = wx.App()
MainFrame(None)
app.MainLoop()