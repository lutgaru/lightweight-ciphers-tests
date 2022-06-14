from logging import error
import os
import subprocess
from sys import platform
import matplotlib
import renode
import matplotlib.pyplot as plt
import numpy as np
from telnetlib import Telnet
import time
from datetime import datetime
#import matplotlib.colors as colors
import matplotlib.pyplot as plt
import csv
import numpy as np
from telnetlib import Telnet

carpeta='multisalto4'
AES, GIFTCOFB, XOODYAK, ASCON128A, ASCON80, ASCON128, GRAIN128, TINYJAMBU192, TINYJAMBU256, TINYJAMBU128, NOCIPHER = range(11)
ciphers=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' GRAIN128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128','NOCIP']


def compileimage(typecif,platform,clean=1,withoptim=1,args=''):
    
    if typecif==GIFTCOFB:
        exito=platform.make("MAKE_WITH_GIFTCOFB=1",with_clean=clean,withoptim=withoptim,args=args+' WCIPHER=0 ')
    elif typecif==XOODYAK:
        exito=platform.make("MAKE_WITH_XOODYAK=1",with_clean=clean,withoptim=withoptim,args=args+' WCIPHER=0 ')
    elif typecif==ASCON128:
        exito=platform.make("MAKE_WITH_ASCON128=1",with_clean=clean,withoptim=withoptim,args=args+' WCIPHER=0 ')
    elif typecif==ASCON128A:
        exito=platform.make("MAKE_WITH_ASCON128A=1",with_clean=clean,withoptim=withoptim,args=args+' WCIPHER=0 ')
    elif typecif==ASCON80:
        exito=platform.make("MAKE_WITH_ASCON80=1",with_clean=clean,withoptim=withoptim,args=args+' WCIPHER=0 ')
    elif typecif==GRAIN128:
        exito=platform.make("MAKE_WITH_GRAIN128=1",with_clean=clean,withoptim=withoptim,args=args+' WCIPHER=0 ')
    elif typecif==TINYJAMBU128:
        exito=platform.make("MAKE_WITH_TINYJAMBU128=1",with_clean=clean,withoptim=withoptim,args=args+' WCIPHER=0 ')
    elif typecif==TINYJAMBU192:
        exito=platform.make("MAKE_WITH_TINYJAMBU192=1",with_clean=clean,withoptim=withoptim,args=args+' WCIPHER=0 ')
    elif typecif==TINYJAMBU256:
        exito=platform.make("MAKE_WITH_TINYJAMBU256=1",with_clean=clean,withoptim=withoptim,args=args+' WCIPHER=0 ')
    elif typecif==NOCIPHER:
        exito=platform.make(with_clean=clean,withoptim=withoptim,args=args+' WCIPHER=1 ')
    else:
        exito=platform.make(with_clean=clean,args=args+' WCIPHER=0 ')
    
    if(exito!=0):
        exit()

def unit_test(platform,cip):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lencu=0
    timetest=600
    pack=1
    print(50*'=')
    print('cipher:',ciphers[cip],"pack:",str(pack))
    ###############compile images##################
    os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test_final/coap-example-client")
    #cip=9
    #nbytes=0
    compileimage(cip,platform,args=' NMUESTRAS='+str(pack)+ ' TIPO=1 ')
    os.chdir(dir_path)
    os.system('cp contiki-ng/examples/coap_cipher_vel_test_final/coap-example-client/coap-example-client.cc2538dk executable/cc2538/cliente')

    os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test_final/coap-example-server")
    compileimage(cip,platform,args=' NMUESTRAS='+str(pack)+ ' TIPO=1 ')
    os.chdir(dir_path)
    os.system('cp contiki-ng/examples/coap_cipher_vel_test_final/coap-example-server/coap-example-server.cc2538dk executable/cc2538/oximetro')
    platform.run(sleep=timetest)

def final_test_1nodo(platform,nodes='oxim'):
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lencu=0
    timetest=1800
    for cip in range(1):
        if cip==6 or cip==5 or cip==3 or cip==4:
            continue
        for pack in [8]:
            #pack=9
            print(50*'=')
            print('cipher:',ciphers[cip],"pack:",str(pack))
            ###############compile images##################
            os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test_final/coap-example-client")
            #cip=9
            #nbytes=0
            compileimage(cip,platform,args=' NMUESTRAS='+str(pack)+ ' TIPO=1 ')
            os.chdir(dir_path)
            os.system('cp contiki-ng/examples/coap_cipher_vel_test_final/coap-example-client/build/cc2538dk/coap-example-client.cc2538dk executable/cc2538/cliente')
            if nodes.find('oxim')!=-1:
                os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test_final/coap-example-server")
                compileimage(cip,platform,args=' NMUESTRAS='+str(pack)+ ' TIPO=1 ')
                os.chdir(dir_path)
                os.system('cp contiki-ng/examples/coap_cipher_vel_test_final/coap-example-server/build/cc2538dk/coap-example-server.cc2538dk executable/cc2538/oximetro')
            if nodes.find('temp')!=-1:
                os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test_final/coap-example-server")
                compileimage(cip,platform,args=' NMUESTRAS='+str(pack)+ ' TIPO=2 ')
                os.chdir(dir_path)
                os.system('cp contiki-ng/examples/coap_cipher_vel_test_final/coap-example-server/build/cc2538dk/coap-example-server.cc2538dk executable/cc2538/termometro')
            if nodes.find('pres')!=-1:
                os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test_final/coap-example-server")
                compileimage(cip,platform,args=' NMUESTRAS='+str(pack)+ ' TIPO=3 ')
                os.chdir(dir_path)
                os.system('cp contiki-ng/examples/coap_cipher_vel_test_final/coap-example-server/build/cc2538dk/coap-example-server.cc2538dk executable/cc2538/esfingo')
            #
            #os.system('echo linux | sudo -S /home/arts1/lightweight-ciphers-tests/reconect.sh')
            #time.sleep(2)
            #
            os.system("renode coap_test_3_saltos_final.resc")
            #return
            





platform=renode.renode()

#unit_test(platform,9)

final_test_1nodo(platform,nodes='oxim-temp-pres')
#os.system('/opt/ti/uniflash/dslite.sh -c cliente.ccxml --post-flash-device-cmd PinReset && /opt/ti/uniflash/dslite.sh -c server.ccxml --post-flash-device-cmd PinResets')
#os.system('renode coap_test.resc')