import os
import time
from telnetlib import Telnet
import subprocess

class renode:
    segundo=32768

    def make(self,defines='',with_clean=1):
        print(with_clean)
        if with_clean==1:
            os.system("make TARGET=cc2538dk clean")
        return os.system("make TARGET=cc2538dk WERROR=0" +defines+ "MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")

    def run(self):
        renoder = subprocess.Popen(["renode", "--disable-xwt", "coap_test.resc", "--port", "33334"])
        print("Esperando..")
        time.sleep(120)
        tn = Telnet("127.0.0.1",33334)
        tn.write("quit\n".encode('ascii'))
        tn.close()
        if (renoder.poll==None):
            renoder.kill()

    def getsize(self):
        return subprocess.run(["size","coap-example-client.cc2538dk"],stdout=subprocess.PIPE,text=True)