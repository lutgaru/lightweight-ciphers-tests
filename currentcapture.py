import os
from telnetlib import Telnet
import subprocess
import serial
import time
import threading
import test_multihop_multiclient

port='/dev/ttyUSB0'
file='extralogs/batterycurrentlog.dat'
ser = serial.Serial(port, 9600,timeout=0.2)
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path+file)
f = open(dir_path+"/"+file,'wb')  

ser.flushInput()
time.sleep(0.2)


while ser.is_open:
    ser.write('FETC?\r\n'.encode('ASCII'))
    data=ser.readline()
    #if(data!=b''):
        #print(data.decode('utf-8'))
        #data=data.decode('utf-8',errors='ignore')
    f.write(data)

    time.sleep(1)
f.close()
ser.close()