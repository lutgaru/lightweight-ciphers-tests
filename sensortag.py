import os
from telnetlib import Telnet
import subprocess
import serial
import time
import threading
import test_multihop_multiclient
class sensortag:

    segundo=65536

    def make(self,defines='',with_clean=1):
        if with_clean==1:
            os.system("make TARGET=cc26x0-cc13x0 clean")
        command="make TARGET=cc26x0-cc13x0 BOARD=sensortag/cc2650 WERROR=0 " +defines+ " MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE"
        print(command)
        return os.system(command)

    def threaduart(self,port,file,timeout,reset):
        ser = serial.Serial(port, 115200,timeout=0.2)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path+file)
        f = open(dir_path+"/"+file,'w')  
        ttimeout=time.time()+timeout
        ser.flushInput()
        time.sleep(0.2)
        os.system(reset)
        print(ttimeout,time.time())
        while ser.is_open:
            data=ser.readline()
            if(data!=b''):
                #print(data.decode('utf-8'))
                data=data.decode('utf-8',errors='ignore')
                f.write(data)
            if(time.time()>ttimeout):
                break
            #time.sleep(1)
        f.close()
        ser.close()
    
    def run(self,program=1,local=1):
        if local:
            if(program):
                exito1=os.system("/opt/ti/uniflash/dslite.sh -c cliente.ccxml -f contiki-ng/examples/coap/coap-example-client/build/cc26x0-cc13x0/sensortag/cc2650/coap-example-client.hex")
                exito2=os.system("/opt/ti/uniflash/dslite.sh -c server.ccxml -f contiki-ng/examples/coap/coap-example-server/build/cc26x0-cc13x0/sensortag/cc2650/coap-example-server.hex")
                if (exito1!=0 or exito2!=0):
                    return -1
            time.sleep(0.2)
            resc="/opt/ti/uniflash/dslite.sh -c cliente.ccxml --post-flash-device-cmd PinReset"
            ress="/opt/ti/uniflash/dslite.sh -c server.ccxml --post-flash-device-cmd PinReset"
            clientthread=threading.Thread(target=self.threaduart,args=("/dev/ttyACM0","clientloguart.dat",45,resc,))#,daemon=True)
            serverthread=threading.Thread(target=self.threaduart,args=("/dev/ttyACM2","serverloguart.dat",45,ress,))#,daemon=True)
            print("= "*80)
            clientthread.start()
            serverthread.start()
            print("Esperando")
            time.sleep(0.2)
            while serverthread.is_alive() or clientthread.is_alive():
                pass
            pass
        else:
            if(program):
                exito1=os.system("/opt/ti/uniflash/dslite.sh -c cliente.ccxml -f contiki-ng/examples/coap/coap-example-client/build/cc26x0-cc13x0/sensortag/cc2650/coap-example-client.hex")
                #exito2=os.system("/opt/ti/uniflash/dslite.sh -c server.ccxml -f contiki-ng/examples/coap/coap-example-server/build/cc26x0-cc13x0/sensortag/cc2650/coap-example-server.hex")
                exito2=test_multihop_multiclient.sendaction('p')
                if (exito1!=0 or exito2!='ok'):
                    return -1
            time.sleep(0.2)
            resc="/opt/ti/uniflash/dslite.sh -c cliente.ccxml --post-flash-device-cmd PinReset"
            #ress="/opt/ti/uniflash/dslite.sh -c server.ccxml --post-flash-device-cmd PinReset"
            resc=test_multihop_multiclient.sendaction('r')
            if (resc!='ok'):
                    return -1
            clientthread=threading.Thread(target=self.threaduart,args=("/dev/ttyACM0","clientloguart.dat",45,resc,))#,daemon=True)
            #serverthread=threading.Thread(target=self.threaduart,args=("/dev/ttyACM2","serverloguart.dat",45,ress,))#,daemon=True)
            print("= "*80)
            clientthread.start()
            #serverthread.start()
            print("Esperando")
            time.sleep(0.2)
            while clientthread.is_alive():
                pass
            pass
    
    def getsize(self):
        return subprocess.run(["size","coap-example-client.cc26x0-cc13x0"],stdout=subprocess.PIPE,text=True)
