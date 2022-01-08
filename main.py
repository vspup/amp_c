# simple program of guide amp AN8031 on J18
# vpupkov@digitsi.com

from tkinter import *
from tkinter import ttk
from time import *

from uart import *


serJ18 = Uart()
dt = 0

fConnectJ18 = False # state cmd Connect
f_amp = False # stat cmd OnOff
f_init_mode = True #if fierst on
fUnblank = False # cmd unblank
fOperate = False # cmd operate
f_work = False
fUart = False # acces to uart
work_regime = 0
mode = 1 # 1- body 2 head
cur_mode = 0


# start windows
window_root = Tk()
window_root.title("tester AMP AN8301")
window_root.rowconfigure(0, weight=1)
window_root.columnconfigure(0, weight=1)
window_root.columnconfigure(1, weight=1)

# J18
frameJ18 = LabelFrame(window_root, text='J18', )
frameJ18.grid(column=0, row=0, sticky='nsew', padx=10, pady=10)
frameJ18.columnconfigure(0, weight=1)
frameJ18.columnconfigure(1, weight=1)
frameJ18.columnconfigure(2, weight=1)
frameJ18.rowconfigure(0, weight=1)

# state
frameState = LabelFrame(frameJ18, text='state', )
frameState.grid(column=0, row=0, padx=10, pady=10, sticky='nsew', columnspan=2, rowspan=2)
labelState = Label(frameState, text="")
labelState.pack()
# mode
frameMode = LabelFrame(frameJ18, text='mode', )
frameMode.grid(column=2, row=0, padx=10, pady=10, sticky='nsew', rowspan=2, columnspan=2)
labelMode = Label(frameMode, text="")
labelMode.pack()

# command
cmdOnOf = Button(frameJ18, text="On", bg="light grey")
cmdOnOf.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
cmdOnOf["state"] = "disabled"
cmdHeadBody = Button(frameJ18, text="ch to ", bg="light grey")
cmdHeadBody.grid(column=1, row=2, sticky='nsew', padx=10, pady=10)
cmdHeadBody["state"] = "disabled"
cmdOperate = Button(frameJ18, text="On Operate", bg="light grey")
cmdOperate.grid(column=2, row=2, sticky='nsew', padx=10, pady=10)
cmdOperate["state"]= "disabled"
cmdUnblank = Button(frameJ18, text="On Unblank", bg="light grey")
cmdUnblank.grid(column=3, row=2, sticky='nsew', padx=10, pady=10)
cmdUnblank["state"]= "disabled"

# serial
SerialsJ18 = ttk.Combobox(frameJ18, values=serJ18.getListPort())
SerialsJ18.grid(column=0, row=3, sticky='nsew', padx=10, pady=10)
SerialsJ18.current(0)
cmdConnectJ18 = Button(frameJ18, text="Connect", bg="light grey")
cmdConnectJ18.grid(column=1, row=3, padx=10, pady=10, sticky='nsew')

# extra inform
labelExtra = Label(frameJ18, text='', )
labelExtra.grid(column=3, row=3, padx=10, pady=10, sticky='nsew', columnspan=2)

# for unblank
# t1 low time
frameUnT1 = LabelFrame(frameJ18, text='T1', )
frameUnT1.grid(column=4, row=0, padx=10, pady=10, sticky='nsew')
labelUnT1 = Entry(frameUnT1, text='', )
labelUnT1.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
cmdT1 = Button(frameUnT1, text='set T1')
cmdT1.grid(column=1, row=0, padx=5, pady=10, sticky='nsew')
labelUnT1['state'] ='disable'
cmdT1['state'] ='disable'
# t2 high time
frameT2 = LabelFrame(frameJ18, text='T2', )
frameT2.grid(column=4, row=1, padx=10, pady=10, sticky='nsew')
labelUnT2 = Entry(frameT2)
labelUnT2.grid(column=0, row=0, padx=5, pady=10, sticky='nsew')
cmdT2 = Button(frameT2, text='set T2')
cmdT2.grid(column=1, row=0, padx=5, pady=10, sticky='nsew')
labelUnT2['state'] ='disable'
cmdT2['state'] ='disable'

fUnCustom = IntVar()
fExtUnblank = IntVar()

def sel():
    global n1, n2    
    print("You selected the option " + str(fUnCustom.get()))
    if(fUnCustom.get() == 1):
        cmdT1['state'] ='normal'
        cmdT2['state'] ='normal'
        labelUnT1['state'] ='normal'
        labelUnT2['state'] ='normal'
        labelUnT1.delete(0, END)
        labelUnT2.delete(0, END)
        labelUnT1.insert(0, str(n1))
        labelUnT2.insert(0, str(n2))
    elif(fUnCustom.get() == 0):
        labelUnT1['state'] ='disable'
        labelUnT2['state'] ='disable'
        cmdT1['state'] ='disable'
        cmdT2['state'] ='disable'
        


enUnCustom = Checkbutton(frameJ18, text='custom Time', variable=fUnCustom, command=sel)
enUnCustom.grid(column=4, row=2, padx=10, pady=10, sticky='nsew')
enUnCustom['state'] = 'disable'

enExUn = Checkbutton(frameJ18, text='custom Time', variable=fExtUnblank)
enExUn.grid(column=4, row=3, padx=10, pady=10, sticky='nsew')




def connectJ18():
    global fConnectJ18
    global f_amp
    global f_init_mode
    global fUnblank
    global fOperate
    global f_work
    global n1, n2
    
    if not fConnectJ18:
        labelState["text"] = ""
        serJ18.connectPort(SerialsJ18.get(), int(115200))
        if str(serJ18.currentPort)!= '0':
            print('Connect ' + str(serJ18.currentPort))
            time.sleep(1)
            
            # mcu detect            
            cmd_MCU = '<20>'
            re = serJ18.transmit(cmd_MCU, 20)
            print(re)
            if re=='a':
                cmdOnOf["state"] = "normal"
                cmdOnOf["text"] = "ON"
                cmdConnectJ18['text'] = "Disconect"
                
                #get current T
                cmd_MCU = '<21>'
                re = serJ18.transmit(cmd_MCU, 5)
                print(re)                
                n1 = int(re)
                cmd_MCU = '<22>'
                re = serJ18.transmit(cmd_MCU, 5)
                print(re)
                n2 = int(re)
                enUnCustom['state'] = 'normal'
                
                fConnectJ18 = True
                labelState["text"] = "connect to MCU"
                
            else:
                cmdConnectJ18['text'] = "Connect"
                serJ18.disconnectPort()
                fConnectJ18 = False
                labelState["text"] = "wrong COM"          
        
    else:
        fConnectJ18 = False
        f_amp = False
        f_init_mode = True
        fOperate = False
        if fUnblank:
            cmd_ = '<188>'
            re = serJ18.transmit(cmd_, 10)
            print (re)
            print ('stop unblank')
            fUnblank = False
            cmdUnblank['text'] = "on Unblank"
            labelUnT1['text'] = 'LOW'
        cmdConnectJ18['text'] = "Connect"
        
        serJ18.disconnectPort()
        print('Disconnect ' + str(serJ18.currentPort))
        cmdOnOf["state"] = "disable"
        cmdHeadBody["state"] = "disable"
        
        cmdOperate["state"] = "disable"
        cmdOperate["text"] = "on Operate"
        fUnblank = False
        
        cmdUnblank["state"] = "disable"
        
        labelState["text"] = ""
        labelMode['text'] = ""
        labelExtra['text'] = ""
        f_work = False
        labelUnT1['state'] ='normal'
        labelUnT2['state'] ='normal'
        labelUnT1.delete(0, END)
        labelUnT2.delete(0, END)
        labelUnT1['state'] ='disable'
        labelUnT2['state'] ='disable'
        cmdT1['state'] ='disable'
        cmdT2['state'] ='disable'
        fUnCustom.set(0)
        n1 = 0
        n2 = 0
        enUnCustom['state'] = 'disable'
        
        


def setOnOff():
    global work_regime
    global fUart
    global f_amp
    global fUnblank
    global fOperate
    global f_work
    fUart = True
    
    if f_amp == False:
        labelState["text"] = "try connect to AMP..."
        cmd_ID = '<113>'
        re = serJ18.transmit(cmd_ID, 200)
        print (re)
        if re=='90':
            work_regime = 1
            f_amp = True
            f_work = True
            cmd_ = '<101>'
            re = serJ18.transmit(cmd_, 10)
            print (re)
            if re!='na':
                print ("cmd ok")
                cmdOnOf['text'] = "OFF"
            
        elif re == "na":
            labelState["text"] = "error connect to AMP"
            print("not answer 113")
    elif f_amp == True:
        if fUnblank:
            cmd_ = '<188>'
            re = serJ18.transmit(cmd_, 10)
            print (re)
            print ('stop unblank')
            fUnblank = False
            cmdUnblank['text'] = "on Unblank"
            
        
        cmd_ = '<100>'
        re = serJ18.transmit(cmd_, 10)
        print (re)
        if re!='na':
            print ("cmd ok")
            work_regime = 0
            cmdOnOf['text'] = "ON"
            f_amp = False
            labelUnT1['text'] = 'LOW'
        
        labelState["text"] = ""
        labelMode['text'] = ""
        labelExtra['text'] = ""
        cmdHeadBody["state"] = "disable"
        cmdOperate["state"] = "disable"
        cmdOperate["text"] = "on Operate"
        cmdUnblank["state"] = "disable"
        cmdUnblank['text'] = "on Unblank"
        fOperate = False
            
    fUart = False



def setMode():
    global fUart
    global mode
    fUart = True
    
    if mode == 1:    
        cmd_B = '<140>'
        re = serJ18.transmit(cmd_B, 10)
        print (re)
        cmdHeadBody['text'] = "ch to BODY"
        mode = 2
    elif mode == 2:    
        cmd_B = '<160>'
        re = serJ18.transmit(cmd_B, 10)
        print (re)
        cmdHeadBody['text'] = "ch to HEAD"
        mode = 1
    
    fUart = False
    
    

def setOperate():
    global fUart
    fUart = True
    global work_regime
    global fOperate
    global fUnblank
    
    if fOperate == False:        
        cmd_ = '<103>'
        re = serJ18.transmit(cmd_, 10)
        print (re)
        fOperate = True
        cmdOperate['text'] = "on Stanby"
        
        
    elif fOperate == True:        
        if fUnblank:
            cmd_ = '<188>'
            re = serJ18.transmit(cmd_, 10)
            print (re)
            print ('stop unblank')
            fUnblank = False
            cmdUnblank['text'] = "on Unblank"
            labelUnT1['text'] = 'LOW'
        cmd_ = '<101>'
        re = serJ18.transmit(cmd_, 10)
        print (re)
        fOperate = False
        cmdOperate['text'] = "on Operate"
        cmd_ = '<188>'
        re = serJ18.transmit(cmd_, 10)
        print (re)
        cmdUnblank['state'] = 'disable' 
        
    fUart = False
    
    
    
def setUnblank():
    global fUnblank
    global fUart
    fUart = True
    if fUnblank == True:
        cmd_ = '<188>'
        re = serJ18.transmit(cmd_, 10)
        print (re)
        cmdUnblank['text'] = "on Unblank"
        labelUnT1['text'] = 'LOW'
        fUnblank=False
        
    elif fUnblank == False: 
        cmd_ = '<177>'
        re = serJ18.transmit(cmd_, 10)
        print (re)
        cmdUnblank['text'] = "off Unblank"
        labelUnT1['text'] = 'HIGH'
        fUnblank=True
        
    fUart = False   


def setT1():
    global n1
    cmd_ = '<3'+str(labelUnT1.get())+'>'
    re = serJ18.transmit(cmd_, 10)
    print (re)
    cmd_ = '<21>'
    re = serJ18.transmit(cmd_, 10)
    print (re)
    n1=int(re)
    labelUnT1.delete(0, END)
    labelUnT1.insert(0, str(n1))
    
    
def setT2():
    global n2
    cmd_ = '<4'+str(labelUnT2.get())+'>'
    re = serJ18.transmit(cmd_, 10)
    print (re)
    cmd_ = '<22>'
    re = serJ18.transmit(cmd_, 10)
    print (re)
    n2=int(re)
    labelUnT2.delete(0, END)
    labelUnT2.insert(0, str(n2))        

cmdConnectJ18['command'] = connectJ18
cmdOnOf['command'] = setOnOff
cmdHeadBody['command'] = setMode
cmdOperate['command'] = setOperate
cmdUnblank['command'] = setUnblank
cmdT1['command'] = setT1
cmdT2['command'] = setT2



def update():
    global dt
    global fUart
    global f_amp
    global cur_mode
    global work_regime
    global mode
    global f_init_mode
    global f_work
    global n1, n2
    
    
    if f_work:
        #labelUnT1.delete(0, END)
        #labelUnT2.delete(0, END)
        #labelUnT1.insert(0, str(n1))
        #labelUnT2.insert(0, str(n2))
        
        if fUart == False:
                
            print("get state")
            st1 = '<111>'
            reState = serJ18.transmit(st1, 10)
                
            if reState == "25":
                labelState.configure(text="wait")
                cmdHeadBody["state"] = "disable"
                work_regime = 1
            elif reState == "29":
                labelState.configure(text="stanby")                
                cmdHeadBody["state"] = "normal"
                #initialize mode
                if f_init_mode:
                    if cur_mode == 1:
                        cmdHeadBody['text'] = "ch to HEAD"
                        mode = 1
                    elif cur_mode == 2:
                        cmdHeadBody['text'] = "ch to BODY"
                        mode = 2
                    f_init_mode = False
                ##                    
                cmdOperate["state"] = "normal"
                work_regime = 2
            elif reState == "3B":
                labelState.configure(text="operate")
                cmdHeadBody["state"] = "disable"
                cmdUnblank['state'] = "normal"
                work_regime = 3                
            elif reState == "20":
                labelState.configure(text="off")
                cmdHeadBody["state"] = "disable"
                work_regime = 0
            else :
                labelState.configure(text="fault" + reState)
                work_regime = 9
                    
            st2 = '<112>'
            reMode = serJ18.transmit(st2, 10)
            if reMode == '60':
                print("body")
                labelMode.configure(text='body')
                cur_mode = 1
            elif reMode == '40':
                labelMode.configure(text='head')
                cur_mode = 2
            else:
                labelMode.configure(text='')
            
            labelExtra.configure(text= reState+' / '+reMode )
            
                    
                    
        
    window_root.after(1000, update)


window_root.after(1000, update())


window_root.mainloop()