# simple program of guide amp AN8031 on J18
# vpupkov@digitsi.com

from tkinter import *
from tkinter import ttk
from time import *

from uart import *


serJ18 = Uart()
dt = 0

fConnectJ18 = False
work_regime = 0

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
frameState.grid(column=0, row=0, padx=10, pady=10, sticky='nsew', columnspan=2)
labelState = Label(frameState, text="")
labelState.pack()
# mode
frameMode = LabelFrame(frameJ18, text='mode', )
frameMode.grid(column=2, row=0, padx=10, pady=10, sticky='nsew')
labelMode = Label(frameMode, text="")
labelMode.pack()

# command
cmdOnOf = Button(frameJ18, text="On", bg="light grey")
cmdOnOf.grid(column=0, row=1, sticky='nsew', padx=10, pady=10)
cmdOnOf["state"] = "disabled"
cmdHeadBody = Button(frameJ18, text="Body", bg="light grey")
cmdHeadBody.grid(column=1, row=1, sticky='nsew', padx=10, pady=10)
cmdHeadBody["state"] = "disabled"
cmdOperate = Button(frameJ18, text="Operate", bg="light grey")
cmdOperate.grid(column=2, row=1, sticky='nsew', padx=10, pady=10)
cmdOperate["state"]= "disabled"

# serial
SerialsJ18 = ttk.Combobox(frameJ18, values=serJ18.getListPort())
SerialsJ18.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
SerialsJ18.current(0)


cmdConnectJ18 = Button(frameJ18, text="Connect", bg="light grey")
cmdConnectJ18.grid(column=1, row=2, padx=10, pady=10, sticky='nsew')




def connectJ18():
    global fConnectJ18
    
    if not fConnectJ18:
        labelState["text"] = ""
        serJ18.connectPort(SerialsJ18.get(), int(115200))
        if str(serJ18.currentPort)!= '0':
            print('Connect ' + str(serJ18.currentPort))
            time.sleep(1)
            
            # mcu detect            
            print ("send 21")
            cmd_MCU = '<21>'
            re = serJ18.transmit(cmd_MCU)
            print(re)
            if re=='a':
                cmdOnOf["state"] = "normal"
                cmdConnectJ18['text'] = "Connected"
                fConnectJ18 = True
                labelState["text"] = "connect to MCU"
            else:
                cmdConnectJ18['text'] = "Connect"
                serJ18.disconnectPort()
                fConnectJ18 = False
                labelState["text"] = "wrong COM"          
        
    else:
        fConnectJ18 = False
        cmdConnectJ18['text'] = "Connect"
        serJ18.disconnectPort()
        print('Disconnect ' + str(serJ18.currentPort))
        fWork = False
        cmdOnOf["state"] = "disable"
        cmdHeadBody["state"] = "disable"
        cmdOperate["state"] = "disable"
        labelState["text"] = ""


def setOnOff():
    global work_regime
    work_regime = 0
    cmd_ID = '<113>'
    re = serJ18.transmit(cmd_ID)
    print (re)
    if re=='90':
        work_regime = 1
    elif re == "na":
        print("not answer 113")
    fUart = False



def setMode():
    global fUart
    fUart = True
    cmd_B = '<177>'
    re = serJ18.send(cmd_B)
    print (re)
    answer.configure(text=re)
    fUart = False

def setOperate():
    global fUart
    fUart = True
    cmd_B = '<188>'
    re = serJ18.send(cmd_B)
    print (re)
    answer.configure(text=re)
    fUart = False

cmdConnectJ18['command'] = connectJ18


cmdOnOf['command'] = setOnOff
cmdHeadBody['command'] = setMode
cmdOperate['command'] = setOperate



def update():
    global dt
    global fUart
    
    if work_regime == 0:
        pass
    elif work_regime == 1:
        print("working")
        
        if fUart == False:
            if 1>0:
                print("get state")
                st1 = '<111>'
                res = serJ18.transmit(st1)
                labelMode.configure(text=res)
                st2 = '<112>'
                res = serJ18.transmit(st2)
                
        
    window_root.after(1000, update)


window_root.after(1000, update())


window_root.mainloop()