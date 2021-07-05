from logging import error
import os
import subprocess
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from telnetlib import Telnet
import time
from datetime import datetime
#import matplotlib.colors as colors
import random
import csv
import sensortag
import renode
import cooja
import test_multihop_multiclient
import matplotlib.pyplot as plt
import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import csv
import numpy as np
from telnetlib import Telnet

AES, GIFTCOFB, XOODYAK, ASCON128A, ASCON80, ASCON128, GRAIN128, TINYJAMBU192, TINYJAMBU256, TINYJAMBU128 = range(10)
RENODE,SENSORTAG,COOJA=range(3)
platforms=['Renode','Sensortag','Cooja']

sizesfilename='sizes_optim2prueba.dat'
velencrypt='velencryptprueba.dat'
veldecrypt='veldecryptprueba.dat'
data_result_dir='/data_results'
coap_dir='/examples/coap'
clientloguart='clientloguart.dat'
serverloguart='serverloguart.dat'
secure_link_times = 'securelinktiming1_tag_3.dat'
secure_link_timesht = 'securelinktiminght1_tag_3.dat'
ciphers=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' GRAIN128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']
ciphers=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']
ciphersl=['AES',' GIFTCOFB',' XOODYAK',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128','ss']
textvs=[]
datavs=[]
bssvs=[]
decvs=[]
hexvs=[]
ciphertimerdifsdecrypt=[]
ciphertimerdifsencrypt=[]
securetimeslink=[]

def compileimage(typecif,platform,clean=1,withoptim=1,nbytes=1):
    
    if typecif==GIFTCOFB:
        exito=platform.make("MAKE_WITH_GIFTCOFB=1",with_clean=clean,withoptim=withoptim,args=' NBYTES='+str(nbytes)+' ')
    elif typecif==XOODYAK:
        exito=platform.make("MAKE_WITH_XOODYAK=1",with_clean=clean,withoptim=withoptim,args=' NBYTES='+str(nbytes)+' ')
    elif typecif==ASCON128:
        exito=platform.make("MAKE_WITH_ASCON128=1",with_clean=clean,withoptim=withoptim,args=' NBYTES='+str(nbytes)+' ')
    elif typecif==ASCON128A:
        exito=platform.make("MAKE_WITH_ASCON128A=1",with_clean=clean,withoptim=withoptim,args=' NBYTES='+str(nbytes)+' ')
    elif typecif==ASCON80:
        exito=platform.make("MAKE_WITH_ASCON80=1",with_clean=clean,withoptim=withoptim,args=' NBYTES='+str(nbytes)+' ')
    elif typecif==GRAIN128:
        exito=platform.make("MAKE_WITH_GRAIN128=1",with_clean=clean,withoptim=withoptim,args=' NBYTES='+str(nbytes)+' ')
    elif typecif==TINYJAMBU128:
        exito=platform.make("MAKE_WITH_TINYJAMBU128=1",with_clean=clean,withoptim=withoptim,args=' NBYTES='+str(nbytes)+' ')
    elif typecif==TINYJAMBU192:
        exito=platform.make("MAKE_WITH_TINYJAMBU192=1",with_clean=clean,withoptim=withoptim,args=' NBYTES='+str(nbytes)+' ')
    elif typecif==TINYJAMBU256:
        exito=platform.make("MAKE_WITH_TINYJAMBU256=1",with_clean=clean,withoptim=withoptim,args=' NBYTES='+str(nbytes)+' ')
    else:
        exito=platform.make(with_clean=clean,args=' NBYTES='+str(nbytes)+' ')
    
    if(exito!=0):
        exit()

def graphic():
    filescrypt=[
        "data_results/cryptonly_Renode_AES_05_28_2021_01:56:43.dat",
        "data_results/cryptonly_Renode_ GIFTCOFB_05_28_2021_01:59:15.dat",
        "data_results/cryptonly_Renode_ XOODYAK_05_28_2021_02:01:47.dat",
        "data_results/cryptonly_Renode_ ASCON128A_05_28_2021_02:04:19.dat",
        "data_results/cryptonly_Renode_ ASCON80_05_28_2021_02:06:51.dat",
        "data_results/cryptonly_Renode_ ASCON128_05_28_2021_02:09:24.dat",
        "data_results/cryptonly_Renode_ TINYJAMBU192_05_28_2021_02:11:57.dat",
        "data_results/cryptonly_Renode_ TINYJAMBU256_05_28_2021_02:14:28.dat",
        "data_results/cryptonly_Renode_ TINYJAMBU128_05_28_2021_02:16:59.dat"
    ]
    filesdecrypt=[
        "data_results/decryptonly_Renode_AES_05_28_2021_01:56:43.dat",
        "data_results/decryptonly_Renode_ GIFTCOFB_05_28_2021_01:59:15.dat",
        "data_results/decryptonly_Renode_ XOODYAK_05_28_2021_02:01:47.dat",
        "data_results/decryptonly_Renode_ ASCON128A_05_28_2021_02:04:19.dat",
        "data_results/decryptonly_Renode_ ASCON80_05_28_2021_02:06:51.dat",
        "data_results/decryptonly_Renode_ ASCON128_05_28_2021_02:09:24.dat",
        "data_results/decryptonly_Renode_ TINYJAMBU192_05_28_2021_02:11:57.dat",
        "data_results/decryptonly_Renode_ TINYJAMBU256_05_28_2021_02:14:28.dat",
        "data_results/decryptonly_Renode_ TINYJAMBU128_05_28_2021_02:16:59.dat"
    ]
    fig,axs=plt.subplots()
    cmap = plt.get_cmap('tab10')
    colors = [cmap(i) for i in np.linspace(0, 1, 10)]
    for i,arch in enumerate(filescrypt):
        data=[]
        datade=[]
        with open(arch,"r") as decv:
            read=csv.reader(decv)
            templist=[list(map(float,x)) for x in list(read)]
            #print(templist)
            data.append(templist)
        with open(filesdecrypt[i],"r") as decv2:
            read2=csv.reader(decv2)
            templist=[list(map(float,x)) for x in list(read2)]
            #print(templist)
            datade.append(templist)
        
    #print(np.roll(data[0],-1))
        print(len(datade[0][0]),len(data[0][0]))
        datade[0].pop(0)
        print(len(datade[0][0]),len(data[0][0]))
        data=np.roll(data[0],-1)
        datade=np.roll(datade[0],-1)
        #print(data)
        #print(datade)
        means=np.mean(data,axis=0)
        stds=np.std(data,axis=0)
        meansde=np.mean(datade,axis=0)
        stdsde=np.std(datade,axis=0)
        #print(means,stds)
        #print(range(0,len(data[2][0][:45])))
        width = 0.35 
        print(i)
        axs.errorbar(np.arange(len(means)),means,yerr=stds,fmt='v-',label=ciphers[i]+" crypt",color=colors[i])
        axs.errorbar(np.arange(len(meansde)),meansde,yerr=stdsde,fmt='x-',label=ciphers[i]+" decrypt",color=colors[i])

    plt.legend()
    axs.set_ylabel("ms")
    axs.set_xlabel("Carga útil en bytes")
    axs.set_title("Velcidad de cifrado y decifrado")
    plt.show()       
    
def graphicsensortag():
    filescrypt=[
        "data_results/cryptonly_Sensortag_AES_05_28_2021_15:54:52.dat",
        "data_results/cryptonly_Sensortag_ GIFTCOFB_05_28_2021_16:00:37.dat",
        "data_results/cryptonly_Sensortag_ XOODYAK_05_28_2021_16:06:23.dat",
        # "data_results/cryptonly_Renode_ ASCON128A_05_28_2021_02:04:19.dat",
        # "data_results/cryptonly_Renode_ ASCON80_05_28_2021_02:06:51.dat",
        # "data_results/cryptonly_Renode_ ASCON128_05_28_2021_02:09:24.dat",
        "data_results/cryptonly_Sensortag_ TINYJAMBU192_05_28_2021_16:29:21.dat",
        "data_results/cryptonly_Sensortag_ TINYJAMBU256_05_28_2021_16:35:05.dat",
        "data_results/cryptonly_Sensortag_ TINYJAMBU128_05_28_2021_16:40:48.dat"
    ]
    filesdecrypt=[
        "data_results/decryptonly_Sensortag_AES_05_28_2021_15:54:52.dat",
        "data_results/decryptonly_Sensortag_ GIFTCOFB_05_28_2021_16:00:37.dat",
        "data_results/decryptonly_Sensortag_ XOODYAK_05_28_2021_16:06:23.dat",
        # "data_results/decryptonly_Renode_ ASCON128A_05_28_2021_02:04:19.dat",
        # "data_results/decryptonly_Renode_ ASCON80_05_28_2021_02:06:51.dat",
        # "data_results/decryptonly_Renode_ ASCON128_05_28_2021_02:09:24.dat",
        "data_results/decryptonly_Sensortag_ TINYJAMBU192_05_28_2021_16:29:21.dat",
        "data_results/decryptonly_Sensortag_ TINYJAMBU256_05_28_2021_16:35:05.dat",
        "data_results/decryptonly_Sensortag_ TINYJAMBU128_05_28_2021_16:40:48.dat"
    ]
    
    fig,axs=plt.subplots()
    cmap = plt.get_cmap('tab10')
    colors = [cmap(i) for i in np.linspace(0, 1, 8)]
    for i,arch in enumerate(filescrypt):
        data=[]
        datade=[]
        with open(arch,"r") as decv:
            read=csv.reader(decv)
            templist=[list(map(float,x)) for x in list(read)]
            #print(templist)
            data.append(templist)
        with open(filesdecrypt[i],"r") as decv2:
            read2=csv.reader(decv2)
            templist=[list(map(float,x)) for x in list(read2)]
            #print(templist)
            datade.append(templist)
        #fig,axs=plt.subplots()
        #print(np.roll(data[0],-1))
        print(len(datade[0][0]),len(data[0][0]))
        for x,datde in enumerate(datade[0]):
            if len(data)<46:
                #datade.pop(i)
                pass
        datade[0].pop(0)
        data[0].pop(0)
        datade[0].pop(0)
        data[0].pop(0)
        #print(datade[0])            
        #print(len(datade[0][1]),len(data[0][1]))
        data=np.roll(data[0],-1)
        datade=np.roll(datade[0],-1)
        #print(data)
        #print(datade)
        means=np.mean(data,axis=0)
        stds=np.std(data,axis=0)
        meansde=np.mean(datade,axis=0)
        stdsde=np.std(datade,axis=0)
        #print(means,stds)
        #print(range(0,len(data[2][0][:45])))
        width = 0.35 
        #axs.plot(np.arange(len(datade[0][0])),datade[0][0])
        print(i)
        axs.errorbar(np.arange(len(means[:-2])),means[:-2],yerr=stds[:-2],fmt='v-',label=ciphersl[i]+" crypt",color=colors[i])
        axs.errorbar(np.arange(len(meansde[:-2])),meansde[:-2],yerr=stdsde[:-2],fmt='x-',label=ciphersl[i]+" decrypt",color=colors[i])
    plt.legend()
    axs.set_ylabel("ms")
    axs.set_xlabel("Carga útil en bytes")
    axs.set_title("Velcidad de cifrado y decifrado para Sensortag")
    plt.show()            

def test_vel_cipher(platform_type=RENODE):
    if(platform_type==SENSORTAG):
        print("usando sensortag")
        platform=sensortag.sensortag()
    elif(platform_type==COOJA):
        platform=cooja.cooja()
    else:
        print("usando renode")
        platform=renode.renode()
    #print(platform[2])
    for lencu in range(0,10):
        now=datetime.now()
        Velcryptonly="data_results/cryptonly_"+platforms[platform_type]+"_"+ciphers[lencu]+"_"+now.strftime("%m_%d_%Y_%H:%M:%S")+".dat"
        Veldecryptonly="data_results/decryptonly_"+platforms[platform_type]+"_"+ciphers[lencu]+"_"+now.strftime("%m_%d_%Y_%H:%M:%S")+".dat"
        timercryptcipher=[]
        timerdecryptcipher=[]
        rtimers=[]
        rtimersht=[]
        #global securetimeslink
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir_path)
        if lencu == 6 or lencu == 3 or lencu == 4 or lencu == 5:
            continue
        ###############compile images##################
        os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test/coap-example-client")
        compileimage(lencu,platform,nbytes=1)
        #if(platform_type==SENSORTAG):
        #    test_multihop_multiclient.sendaction('m-'+str(x))
        #else:
        os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test/coap-example-server")
        compileimage(lencu,platform,nbytes=1)
        os.chdir(dir_path)
        #for x in range(1,46):
            
            ###############compile images##################
            #os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test/coap-example-client")
            #compileimage(lencu,platform,clean=0,nbytes=x)
            #if(platform_type==SENSORTAG):
            #    test_multihop_multiclient.sendaction('m-'+str(x))
            #else:
            # os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test/coap-example-server")
            # compileimage(lencu,platform,clean=0,nbytes=x)
            # os.chdir(dir_path)
            ###############run simulator##################
        timercrypt=[]
        timerdecrypt=[]
        platform.run()
    
        ###############extract values from log files##################
        #print("cifrador:",ciphers[lencu],"muestra:",x)
        time.sleep(1)
        #----------------client----------------#
        clientuart=open(clientloguart,'r',errors='replace')
        lines=clientuart.readlines()
        clientuart.close()
        acti=False
        for line in lines:
            lined=line.split(",")
            if(lined[0]!='#' and acti==False):
                continue
            else:
                acti=True
            if(lined[0]=="decrypt"):
                try:
                    n2=int(lined[2][:-1])
                    n1=int(lined[1][1:])
                    timerdecrypt.append((1000*(n2-n1))/platform.segundo)
                except:
                    timercrypt.append(0)
                    #continue
            if(lined[0]=='='):
                timerdecryptcipher.append(timerdecrypt)
                timerdecrypt=[]
        os.remove(clientloguart)
        serveruart=open(serverloguart,'r',errors='replace')
        lines=serveruart.readlines()
        serveruart.close()
        nb="na"
        acti=False
        for line in lines:
            lined=line.split(",")
            if(lined[0]!='#' and acti==False):
                continue
            else:
                acti=True
            if(lined[0]=="encrypt"):
                try:
                    n2=int(lined[2][:-1])
                    n1=int(lined[1][1:])
                    timercrypt.append((1000*(n2-n1))/platform.segundo)
                except:
                    timercrypt.append(0)
                    #continue
                
            if(lined[0]=="Nbytes"):
                nb=lined[1]
            if(lined[0]=='='):
                timercryptcipher.append(timercrypt)
                timercrypt=[]
        print(nb)
        os.remove(serverloguart)
        #print(timerdiffl)
        #print(rtimer)
        #platform.run()
            #return
        #return
        
       
        print(timercryptcipher)
        #print(rtimers)
        print(timerdecryptcipher)
        #print(rtimersht)
        with open(Velcryptonly,'w') as f:
            wr = csv.writer(f)
            wr.writerows(timercryptcipher)
        with open(Veldecryptonly,'w') as f:
            wr = csv.writer(f)
            wr.writerows(timerdecryptcipher)

if __name__ == "__main__":
    
    #testvelocitycipher()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    # for x in range(10):
    #     vel=[]
    #     for y in range(random.randint(3,10)):
    #         vel.append(random.randint(1,10))
    #     ciphertimerdifsdecrypt.append(vel)
    #     ciphertimerdifsencrypt.append(vel)
    # print(ciphertimerdifsdecrypt)
    # print(ciphertimerdifsencrypt)
    #np.save(veldecrypt,ciphertimerdifsdecrypt)
    
    #np.save(velencrypt,ciphertimerdifsencrypt)
    #testvelocitycipher()
    # for test in range(10):
    #    print("pasada",test)
    #    test_secure_link(RENODE)
    #testimagessize(SENSORTAG,withoptim=0)

    #testvelocitycipher(SENSORTAG,withoptim=0)
    #plataform=sensortag.sensortag()
    plataform=sensortag.sensortag()
    #os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test/coap-example-client")
    #compileimage(GRAIN128,plataform,clean=1)
    #os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test/coap-example-server")
    #compileimage(GRAIN128,plataform,clean=1)
    # plataform.run(1,1)
    # os.chdir(dir_path)
    #platform=cooja.cooja()
    #test_vel_cipher(SENSORTAG)
    graphicsensortag()
    #graphic()
    #platform.run()
    #testimagessize(RENODE)
    #plotvelcipher(ciphertimerdifsencrypt,ciphertimerdifsdecrypt)
    pass