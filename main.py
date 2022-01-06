# simple program of guide amp AN8031 on J18
# vpupkov@digitsi.com

from tkinter import *
from tkinter import ttk
from time import *

from uart import *


serJ18 = Uart()
dt = 0

fConnectJ18 = False
fWork = False
fUart = False

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

# command
ScanID = Button(frameJ18, text="get ID", bg="light grey")
ScanID.grid(column=0, row=1, sticky='nsew', padx=10, pady=10)
UnblankON = Button(frameJ18, text="ON Unblank", bg="light grey")
UnblankON.grid(column=1, row=1, sticky='nsew', padx=10, pady=10)
UnblankOFF = Button(frameJ18, text="OFF Unblank", bg="light grey")
UnblankOFF.grid(column=2, row=1, sticky='nsew', padx=10, pady=10)
cmdON = Button(frameJ18, text="ON", bg="light grey")
cmdON.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
cmdOFF = Button(frameJ18, text="OFF", bg="light grey")
cmdOFF.grid(column=1, row=2, sticky='nsew', padx=10, pady=10)
cmdOP = Button(frameJ18, text="OPERATE", bg="light grey")
cmdOP.grid(column=2, row=2, sticky='nsew', padx=10, pady=10)
cmdHEAD = Button(frameJ18, text="HEAD", bg="light grey")
cmdHEAD.grid(column=0, row=3, sticky='nsew', padx=10, pady=10)
cmdBODY = Button(frameJ18, text="BODY", bg="light grey")
cmdBODY.grid(column=1, row=3, sticky='nsew', padx=10, pady=10)
answer = Label(frameJ18, text="- / -")
answer.grid(column=2, row=3, padx=10, pady=10, sticky='nsew')
# state
state0 = Label(frameJ18, text="Current State")
state0.grid(column=0, row=0, padx=10, pady=10, sticky='nw')
state1 = Label(frameJ18, text="s1")
state1.grid(column=1, row=0, padx=10, pady=10, sticky='n')
state2 = Label(frameJ18, text="s2")
state2.grid(column=2, row=0, padx=10, pady=10, sticky='ne')
# serial
SerialsJ18 = ttk.Combobox(frameJ18, values=serJ18.getListPort())
SerialsJ18.grid(column=0, row=5, sticky='sw', padx=10, pady=10)
SerialsJ18.current(0)

r_var = BooleanVar()
r1 = Checkbutton(frameJ18, text='state', variable=r_var, onvalue=1, offvalue=0)
r1.grid(column=1, row=5, sticky='sw', padx=10, pady=10)


ConnectJ18 = Button(frameJ18, text="Connect", bg="light grey")
ConnectJ18.grid(column=2, row=5, padx=10, pady=10, sticky='se')




def connectJ18():
    global fConnectJ18
    global fWork
    if not fConnectJ18:
        serJ18.connectPort(SerialsJ18.get(), int(115200))
        print('Connect ' + str(serJ18.currentPort))
        ConnectJ18['text'] = "Connected"
        fConnectJ18 = True
        time.sleep(1)
        fWork = True
    else:
        fConnectJ18 = False
        ConnectJ18['text'] = "Connect"
        serJ18.disconnectPort()
        print('Disconnect ' + str(serJ18.currentPort))
        fWork = False


def getID():
    global fUart
    fUart = True
    cmd_ID = '<113>'
    re = serJ18.transmit(cmd_ID)
    print (re)
    answer.configure(text=re)
    fUart = False

def setON():
    global fUart
    fUart = True
    cmd_A = '<101>'
    re = serJ18.transmit(cmd_A)
    print (re)
    answer.configure(text=re)
    fUart = False
    
def setOP():
    global fUart
    fUart = True
    cmd_A = '<103>'
    re = serJ18.transmit(cmd_A)
    print (re)
    answer.configure(text=re)
    fUart = False

def setOFF():
    global fUart
    fUart = True
    cmd_A = '<100>'
    re = serJ18.transmit(cmd_A)
    print (re)
    answer.configure(text=re)
    fUart = False

def setHEAD():
    global fUart
    fUart = True
    cmd_B = '<140>'
    re = serJ18.transmit(cmd_B)
    print (re)
    answer.configure(text=re)
    fUart = False

def setBODY():
    global fUart
    fUart = True
    cmd_B = '<160>'
    re = serJ18.transmit(cmd_B)
    print (re)
    answer.configure(text=re)
    fUart = False

def setUn():
    global fUart
    fUart = True
    cmd_B = '<177>'
    re = serJ18.send(cmd_B)
    print (re)
    answer.configure(text=re)
    fUart = False

def setDUn():
    global fUart
    fUart = True
    cmd_B = '<188>'
    re = serJ18.send(cmd_B)
    print (re)
    answer.configure(text=re)
    fUart = False

ConnectJ18['command'] = connectJ18


ScanID['command'] = getID
cmdON['command'] = setON
cmdHEAD['command'] = setHEAD
cmdOFF['command'] = setOFF
cmdOP['command'] = setOP
cmdBODY['command'] = setBODY
UnblankON['command'] = setUn
UnblankOFF['command'] = setDUn



def update():
    global dt
    global fUart
    
    if fWork:
        print("work")
        state1.configure(text='')
        state2.configure(text='')
        if fUart == False:
            if r_var.get():
                print("get state")
                st1 = '<111>'
                res = serJ18.transmit(st1)
                state1.configure(text=res)
                st2 = '<112>'
                res = serJ18.transmit(st2)
                state2.configure(text=res)
        
    window_root.after(1000, update)


window_root.after(1000, update())


window_root.mainloop()