import time
from machine import Pin
from ir_rx.print_error import print_error
from ir_rx.nec import NEC_8

IRdict = {
    69: "Power", 70: "vol+", 71: "stop", 68: "<<", 64: ">||", 67: ">>", 
    7: "v", 21: "vol-", 9: "^", 22: 0, 25: "=", 13: "rept", 12: 1, 24: 2, 
    94: 3, 8: 4, 28: 5, 90: 6, 66: 7, 82: 8, 74: 9
}
newCommand = []
beginRecord = False
endRecord = False

irPin = 17

my_IR = Pin(irPin, Pin.IN)

def callback(cmd, x, y):
    global newCommand
    global beginRecord
    global endRecord
    
    #print(cmd)
    
    if cmd == 69:
        beginRecord = True
        newCommand = []
        endRecord = False
    
    if beginRecord and cmd != -1:
        if cmd in IRdict:
            newCommand.append(IRdict[cmd])
    
    if cmd == 25:
        endRecord = True
        beginRecord = False
    
    
IR = NEC_8(my_IR, callback)

try:
    while True:
        if endRecord == True:
            print(newCommand)
            endRecord = False
    
except KeyboardInterrupt:
    IR.close()
    print("Program Terminated")


