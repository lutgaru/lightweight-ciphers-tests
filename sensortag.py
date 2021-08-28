from datetime import datetime
import os
from telnetlib import Telnet
import subprocess
import serial
import time
import threading
import test_multihop_multiclient
class sensortag:

    segundo=65536
    nombre='sensortag'

    def make(self,defines='',with_clean=1,withoptim=1, args=''):
        if with_clean==1:
            os.system("make TARGET=cc26x0-cc13x0 clean")
        if withoptim:
            defines=defines+' WITH_OPTIMIZATION=1 '
        if args:
            defines=defines+args
        command="make TARGET=cc26x0-cc13x0 BOARD=sensortag/cc2650 WERROR=0 " +defines+ " MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE"
        print(command)
        return os.system(command)

    def puertouart(self,port):
        puerto=os.popen('readlink -f '+port).read()
        numero=int(puerto[puerto.find('ACM')+3:])-1
        return puerto[:puerto.find('ACM')+3]+str(numero)

    def threaduart(self,port,file,timeout,reset):
        ser = serial.Serial(port, 115200,timeout=0.2)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path+file)
        f = open(dir_path+"/"+file,'wb')  
        ttimeout=time.time()+timeout
        ser.flushInput()
        time.sleep(0.2)
        os.system(reset)
        f.write((datetime.now().strftime('TT,%m,%d,%y,%H,%M,%S,%f')+'\n').encode('ascii'))
        print(ttimeout,time.time())
        while ser.is_open:
            data=ser.read(size=ser.in_waiting)
            #if(data!=b''):
                #print(data.decode('utf-8'))
                #data=data.decode('utf-8',errors='ignore')
            f.write(data)
            if(time.time()>ttimeout):
                break
            #time.sleep(1)
        f.close()
        ser.close()
    
    def run(self,program=1,local=1,sleep=300,nodes='oxim'):
        if local:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            os.chdir(dir_path)
            if(program):
                
                exito1=os.system("/opt/ti/uniflash/dslite.sh -c Cliente.ccxml -f executable/cc2650/cliente/coap-example-client.hex")
                if nodes.find('oxim')!=-1:
                    exito2=os.system("/opt/ti/uniflash/dslite.sh -c oximetro.ccxml -f executable/cc2650/oximetro/coap-example-server.hex")
                if nodes.find('temp')!=-1:
                    exito2=os.system("/opt/ti/uniflash/dslite.sh -c Termometro.ccxml -f executable/cc2650/termometro/coap-example-server.hex")
                if nodes.find('pres')!=-1:
                    exito2=os.system("/opt/ti/uniflash/dslite.sh -c presion.ccxml -f executable/cc2650/esfingo/coap-example-server.hex")
                
                if (exito1!=0 or exito2!=0):
                    return -1
            time.sleep(0.2)
            resc="/opt/ti/uniflash/dslite.sh -c Cliente.ccxml --post-flash-device-cmd PinReset"
            clientthread=threading.Thread(target=self.threaduart,args=(self.puertouart("/dev/ttyCLIENTE"),"clientloguart.dat",sleep,resc,))
            if nodes.find('oxim')!=-1:
                ress="/opt/ti/uniflash/dslite.sh -c oximetro.ccxml --post-flash-device-cmd PinReset"
                oxithread=threading.Thread(target=self.threaduart,args=(self.puertouart("/dev/ttyOXIMETRO"),"oximloguart.dat",sleep,ress,))
            if nodes.find('temp')!=-1:
                ress="/opt/ti/uniflash/dslite.sh -c Termometro.ccxml --post-flash-device-cmd PinReset"
                tempthread=threading.Thread(target=self.threaduart,args=(self.puertouart("/dev/ttyTERMOMETRO"),"temploguart.dat",sleep,ress,))
            if nodes.find('pres')!=-1:
                ress="/opt/ti/uniflash/dslite.sh -c presion.ccxml --post-flash-device-cmd PinReset"
                presthread=threading.Thread(target=self.threaduart,args=(self.puertouart("/dev/ttyPRESION"),"presloguart.dat",sleep,ress,))
            #return
           
            print("= "*80)
            
            if nodes.find('oxim')!=-1:
                oxithread.start()
            if nodes.find('temp')!=-1:
                tempthread.start()
            if nodes.find('pres')!=-1:
                presthread.start()
            clientthread.start()
            
            print("Esperando")
            time.sleep(0.2)
            while clientthread.is_alive():
                pass
            pass
        else:
            if(program):
                exito1=os.system("/opt/ti/uniflash/dslite.sh -c cliente.ccxml -f contiki-ng/examples/coap/coap-example-client/build/cc26x0-cc13x0/sensortag/cc2650/coap-example-client.hex")
                #exito2=os.system("/opt/ti/uniflash/dslite.sh -c server.ccxml -f contiki-ng/examples/coap/coap-example-server/build/cc26x0-cc13x0/sensortag/cc2650/coap-example-server.hex")
                exito2=test_multihop_multiclient.sendaction('p')
                exit()
                if (exito1!=0):
                    return -1
            time.sleep(0.2)
            resc="/opt/ti/uniflash/dslite.sh -c cliente.ccxml --post-flash-device-cmd PinReset"
            os.system("/opt/ti/uniflash/dslite.sh -c server2.ccxml --post-flash-device-cmd PinReset")
            test_multihop_multiclient.sendaction('r')
            #if (resc!=0):
            #        return -1
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
