import os
import time
from telnetlib import Telnet
import subprocess

class renode:
    segundo=32768
    nombre='renode'

    def make(self,defines='',with_clean=1,withoptim=1, args=''):
        #print(with_clean)
        if with_clean==1:
            os.system("make TARGET=cc2538dk clean")
        if withoptim:
            defines=defines+' WITH_OPTIMIZATION=1 '
        if args!='':
            defines=defines+args
        command="make TARGET=cc2538dk WERROR=0 " +defines+ " MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE"
        print(command)
        return os.system(command)

    def run(self,program=1,sleep=120):
        renoder = subprocess.Popen(["renode", "--disable-xwt", "coap_test.resc", "--port", "33334"])
        print("Esperando..")
        time.sleep(sleep)
        tn = Telnet("127.0.0.1",33334)
        tn.write("quit\n".encode('ascii'))
        tn.close()
        time.sleep(0.2)
        if (renoder.poll==None):
            renoder.kill()

    def getsize(self):
        return subprocess.run(["size","coap-example-client.cc2538dk"],stdout=subprocess.PIPE,text=True)