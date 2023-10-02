import re
import threading

import wx
import mouse
import keyboard

class LeftPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        # self.SetBackgroundColour(wx.BLUE)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        #coordinate
        coor_stt = wx.StaticText(self,label="Coordinate")
        left_sizer.Add(coor_stt,0,wx.EXPAND|wx.ALL,10)

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
        self.stop_txt = wx.TextCtrl(self)
        self.stop_txt.Bind(wx.EVT_KEY_DOWN, self.UpdateText)
        stop_unit = wx.StaticText(self,label = "Clicks")

        #current
        curclick_stt = wx.StaticText(self,label="Current")
        self.curclick_txt = wx.TextCtrl(self)
        self.curclick_txt.Bind(wx.EVT_KEY_DOWN, self.UpdateText)
        curclick_unit = wx.StaticText(self,label = "Clicks")

        #stop after
        stoptime_stt = wx.StaticText(self,label="Stop After")
        self.stoptime_txt = wx.TextCtrl(self)
        self.stoptime_txt.Bind(wx.EVT_KEY_DOWN, self.UpdateText)
        stoptime_unit = wx.StaticText(self,label = "mins")

        #current
        curtime_stt = wx.StaticText(self,label="Current")
        self.curtime_txt = wx.TextCtrl(self)
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
        left_sizer.Add(checkbox, 0, wx.CENTER | wx.ALL, 0)

        self.SetSizer(left_sizer)
        self.SetValue()

    def SetValue(self):
        self.inter_txt.SetValue('600')
        self.stop_txt.SetValue('0')
        self.curclick_txt.SetValue('0')
        self.stoptime_txt.SetValue('0')
        self.curtime_txt.SetValue('0')

    def UpdateText(self,evt):
        if evt.GetKeyCode()>=48 and evt.GetKeyCode()<=57:
            print(evt.GetKeyCode())
            evt.Skip()
    def GetData(self):
        inter = self.inter_txt.GetValue()
        stop = self.stop_txt.GetValue()
        curclick = self.curclick_txt.GetValue()
        stoptime = self.stoptime_txt.GetValue()
        curtime = self.curtime_txt.GetValue()
        return {'inter':int(inter),'stop':int(stop),'curclick':int(curclick),'stoptime':int(stoptime),'curtime':int(curtime)}
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
        self.maintext= wx.TextCtrl(self,style = wx.TE_MULTILINE)
        right_sizer.Add(self.maintext, 1, wx.EXPAND | wx.ALL, 10)

        #count
        cnt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        cnt_stt = wx.StaticText(self,label="Count")
        cnt_txt = wx.TextCtrl(self)
        cnt_sizer.Add(cnt_stt,0,wx.ALL|wx.EXPAND,5)
        cnt_sizer.Add(cnt_txt, 0, wx.ALL | wx.EXPAND, 5)
        right_sizer.Add(cnt_sizer, 0, wx.EXPAND | wx.ALL, 0)

        #button
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_btn = wx.Button(self,label='Save')

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

        self.maintext.SetValue('''x: 277 y: 369
x: 277 y: 369
x: 282 y: 185
x: 282 y: 185
x: 179 y: 109
x: 179 y: 109
x: 131 y: 343
x: 131 y: 343''')

    def LoadData(self,evt):
        self.parent.StartRecode()

    def UpdateData(self,mouse_events):
        save_x = 0
        save_y = 0
        data_save = ''
        for evt in mouse_events:
            # print(type(evt))
            if type(evt) is mouse._mouse_event.MoveEvent:
                # print('x: ', evt.x, ' y: ', evt.y)
                save_x = evt.x
                save_y = evt.y

            elif type(evt) is mouse._mouse_event.ButtonEvent:
                # print(evt)
                data_save+='x: '+str(save_x)+' y: '+str(save_y)+'\n'
        print(data_save)
        self.maintext.SetValue(data_save)

    def GetData(self):
        data = self.maintext.GetValue()
        list_data = re.split('\n',data)
        list_return = []
        for line in list_data:
            mathdata = re.match('x:\s+(\d+)\s+y:\s+(\d+)',line)
            if mathdata:
                list_return.append({'x':int(mathdata.groups()[0]),'y':int(mathdata.groups()[1])})
        return list_return
class MainFrame(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,title='Auto Click')
        self.SetSize(500,500)

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
        bottom_sizer.Add(start_btn,1,wx.ALL|wx.CENTER,10)
        bottom_sizer.Add(cancel_btn, 1, wx.ALL | wx.CENTER, 10)
        main_sizer.Add(bottom_sizer, 0, wx.ALL | wx.CENTER , 0)

        self.SetSizer(main_sizer)

        self.Show()

        self.mouse_events = []

    def StartRecode(self):
        print('StartRecode')
        mouse.hook(self.mouse_events.append)
        keyboard.wait("Esc")
        mouse.unhook(self.mouse_events.append)
        print(self.mouse_events)
        self.rightpanel.UpdateData(self.mouse_events)
        self.mouse_events = []

    def RunRecord(self,evt):
        data_setup = self.leftpanel.GetData()
        data_record = self.rightpanel.GetData()
        mouse_evt = []
        time_idx = 1
        for data in data_record:
            mouse_evt.append(mouse.MoveEvent(data['x'],data['y'],time_idx))
            time_idx+=data_setup['inter']/1000
        print(mouse_evt)
        m_thread = threading.Thread(target=lambda: mouse.play(mouse_evt))
        m_thread.start()

app = wx.App()
MainFrame(None)
app.MainLoop()