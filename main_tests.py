import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from telnetlib import Telnet
import time
from datetime import datetime
import random
import csv
import sensortag
import renode
import cooja
import test_multihop_multiclient

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
textvs=[]
datavs=[]
bssvs=[]
decvs=[]
hexvs=[]
ciphertimerdifsdecrypt=[]
ciphertimerdifsencrypt=[]
securetimeslink=[]

def compileimage(typecif,platform,clean=1,withoptim=1):
    
    if typecif==GIFTCOFB:
        exito=platform.make("MAKE_WITH_GIFTCOFB=1",with_clean=clean,withoptim=withoptim)
    elif typecif==XOODYAK:
        exito=platform.make("MAKE_WITH_XOODYAK=1",with_clean=clean,withoptim=withoptim)
    elif typecif==ASCON128:
        exito=platform.make("MAKE_WITH_ASCON128=1",with_clean=clean,withoptim=withoptim)
    elif typecif==ASCON128A:
        exito=platform.make("MAKE_WITH_ASCON128A=1",with_clean=clean,withoptim=withoptim)
    elif typecif==ASCON80:
        exito=platform.make("MAKE_WITH_ASCON80=1",with_clean=clean,withoptim=withoptim)
    elif typecif==GRAIN128:
        exito=platform.make("MAKE_WITH_GRAIN128=1",with_clean=clean,withoptim=withoptim)
    elif typecif==TINYJAMBU128:
        exito=platform.make("MAKE_WITH_TINYJAMBU128=1",with_clean=clean,withoptim=withoptim)
    elif typecif==TINYJAMBU192:
        exito=platform.make("MAKE_WITH_TINYJAMBU192=1",with_clean=clean,withoptim=withoptim)
    elif typecif==TINYJAMBU256:
        exito=platform.make("MAKE_WITH_TINYJAMBU256=1",with_clean=clean,withoptim=withoptim)
    else:
        exito=platform.make(with_clean=clean)
    
    if(exito!=0):
        exit()

def bar_plot(ax, data, error=None ,colors=None, total_width=0.8, single_width=1, legend=True):

    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            if error is None:
                bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])
            else:
                #print(error[i][x], i, x)
                bar = ax.bar(x + x_offset, y,yerr=error[i][x], width=bar_width * single_width, color=colors[i % len(colors)],capsize=10)

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())   

def appendsize(platform):
    #sizestr=subprocess.run(["size","coap-example-client.cc2538dk"],stdout=subprocess.PIPE,text=True)
    sizestr=platform.getsize()
    sizesvals=sizestr.stdout.split("\n")[1].split("\t")
    print(sizestr.stdout.split("\n"))
    print(sizesvals)
    textvs.append(int(sizesvals[0]))
    datavs.append(int(sizesvals[1]))
    bssvs.append(int(sizesvals[2]))
    decvs.append(int(sizesvals[3]))
    #hexvs.append(int(sizesvals[4]))

def plotvelcipher(encryptv,decryptv):
    global ciphers
    ciphersdevelmean=[]
    ciphersenvelmean=[]
    ciphersenvelstd=[]
    ciphersdevelstd=[]
    for encv in encryptv:
        ciphersenvelmean.append(np.mean(encv))
        print(encv)
        ciphersenvelstd.append(np.std(encv))
    for decv in decryptv:
        ciphersdevelmean.append(np.mean(decv))
        ciphersdevelstd.append(np.std(decv))
    fig, ax = plt.subplots()
    data={
        "Encryptado":ciphersenvelmean,
        "Desencryptado":ciphersdevelmean,
    }
    errordata=[ciphersenvelstd,ciphersdevelstd]
    bar_plot(ax,data,errordata, total_width=.8, single_width=.9)
    ax.set_ylabel('ms')
    x_pos=np.arange(len(ciphers))
    ax.set_xticks(x_pos)
    ax.set_xticklabels(ciphers)
    ax.set_title('Velocidad de Desencriptado')
    ax.yaxis.grid(True)
    plt.show()

def plotvellink(vellinks,vellinksht):
    global ciphers
    ciphersenvelmean=[]
    ciphersenvelstd=[]
    ciphersenvelmeanht=[]
    ciphersenvelstdht=[]
    for encv in vellinks:
        #print(np.mean(encv))
        ciphersenvelmean.append(np.mean(encv))
        #print(np.std(encv))
        ciphersenvelstd.append(np.std(encv))
    for encv in vellinksht:
        #print(np.mean(encv))
        ciphersenvelmeanht.append(np.mean(encv))
        #print(np.std(encv))
        ciphersenvelstdht.append(np.std(encv))
    fig, ax = plt.subplots()
    usages={
        "Tiempo Para Seguro":ciphersenvelmean,
        "Tiempo Handshake":ciphersenvelmeanht,
    }
    bar_plot(ax, usages,[ciphersenvelstd,ciphersenvelstdht], total_width=.8, single_width=.9)
    #plt.plot(ciphers,[textvs,datavs],kind="bar")
    ax.set_ylabel('ms')
    ax.set_title('Velocidad de enlace seguro')
    ax.yaxis.grid(True)
    plt.xticks(range(10),ciphers)
    plt.show()

def testimagessize(platform_type=RENODE,withoptim=1):
    global textvs,datavs,bssvs,decvs,hexvs
    if(platform_type==SENSORTAG):
        platform=sensortag.sensortag()
    elif(platform_type==COOJA):
        platform=cooja.cooja()
    else:
        platform=renode.renode()
    now=datetime.now()
    sizesfilename='sizes_'+platforms[platform_type]+'_'+now.strftime("%m_%d_%Y_%H:%M:%S")+'.dat'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path+data_result_dir)
    print("holaa")
    if os.path.isfile(sizesfilename):
        #print("holaa")
        sizesback = np.loadtxt(sizesfilename)
        textvs=sizesback[0,:]
        datavs=sizesback[1,:]
        bssvs=sizesback[2,:]
        decvs=sizesback[3,:]
        #hexvs=sizesback[4,:]
    else:
        os.chdir(dir_path+"/contiki-ng/examples/coap/coap-example-client")
        print(dir_path+"/contiki-ng/examples/coap/coap-example-client")
        for x in range(10):
            compileimage(x,platform,withoptim=withoptim)
            appendsize(platform)
        os.chdir(dir_path)
        np.savetxt(sizesfilename,[textvs,datavs,bssvs,decvs])
    fig, ax = plt.subplots()
    sizesv={
        "text":textvs,
        "data":datavs,
        "bss":bssvs,
        "dec":decvs,
        #"hex":hexvs,
    }
    romusage=textvs+datavs
    ramusage=datavs+bssvs
    usages={
        "RAM":ramusage,
        "ROM":romusage,
    }
    bar_plot(ax, usages, total_width=.8, single_width=.9)
    #plt.plot(ciphers,[textvs,datavs],kind="bar")
    plt.xticks(range(10),ciphers)
    plt.show()


def testvelocitycipher(platform_type=RENODE,withoptim=1):
    global ciphertimerdifs
    global ciphertimerdifsdecrypt
    global ciphertimerdifsencrypt
    if(platform_type==SENSORTAG):
        platform=sensortag.sensortag()
    elif(platform_type==COOJA):
        platform=cooja.cooja()
    else:
        platform=renode.renode()
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path+data_result_dir)
    now=datetime.now()
    velencrypt="data_results/velencryptprueba"+platforms[platform_type]+now.strftime("%m_%d_%Y_%H:%M:%S")+".dat"
    veldecrypt="data_results/veldecryptprueba"+platforms[platform_type]+now.strftime("%m_%d_%Y_%H:%M:%S")+".dat"
    for x in range(10):
        if platform_type==SENSORTAG and (x==ASCON128 or x== ASCON128A or x==ASCON80):
            continue
        ###############compile images##################
        os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test/coap-example-client")
        compileimage(x,platform,withoptim=withoptim)
        os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test/coap-example-server")
        compileimage(x,platform,withoptim=withoptim)
        os.chdir(dir_path)
        ###############run renode emulator##################
        platform.run()
        ###############extract values from log files##################
        timerdiffe=[]
        timerdiffd=[]
        time.sleep(1)
        #----------------client----------------#
        clientuart=open(clientloguart,'r')
        lines=clientuart.readlines()
        clientuart.close
        os.remove(clientloguart)
        for line in lines:
            if(line.find("decrypt1")!=-1):
                t1int=int(line[line.find("decrypt1")+8:])
            if(line.find("decrypt2")!=-1):
                t2int=int(line[line.find("decrypt2")+8:])
                timerdiffd.append(((t2int-t1int)/platform.segundo)*1000)
            if(line.find("encrypt1")!=-1):
                t1int=int(line[line.find("encrypt1")+8:])
            if(line.find("encrypt2")!=-1):
                t2int=int(line[line.find("encrypt2")+8:])
                timerdiffe.append(((t2int-t1int)/platform.segundo)*1000)
        #----------------server----------------#
        serveruart=open(serverloguart,'r')
        lines=serveruart.readlines()
        serveruart.close
        os.remove(serverloguart)
        for line in lines:
            if(line.find("decrypt1")!=-1):
                t1int=int(line[line.find("decrypt1")+8:])
            if(line.find("decrypt2")!=-1):
                t2int=int(line[line.find("decrypt2")+8:])
                timerdiffd.append(((t2int-t1int)/platform.segundo)*1000)
            if(line.find("encrypt1")!=-1):
                t1int=int(line[line.find("encrypt1")+8:])
            if(line.find("encrypt2")!=-1):
                t2int=int(line[line.find("encrypt2")+8:])
                timerdiffe.append(((t2int-t1int)/platform.segundo)*1000)
        print(timerdiffe,timerdiffd)
        ciphertimerdifsdecrypt.append(timerdiffd)
        ciphertimerdifsencrypt.append(timerdiffe)
    with open(velencrypt,'w') as f:
        wr = csv.writer(f)
        wr.writerows(ciphertimerdifsencrypt)
    with open(veldecrypt,'w') as f:
        wr = csv.writer(f)
        wr.writerows(ciphertimerdifsdecrypt)
    plotvelcipher(ciphertimerdifsencrypt,ciphertimerdifsdecrypt)

def test_secure_link(platform_type=RENODE):
    if(platform_type==SENSORTAG):
        print("usando sensortag")
        platform=sensortag.sensortag()
    elif(platform_type==COOJA):
        platform=cooja.cooja()
    else:
        print("usando renode")
        platform=renode.renode()
    #print(platform[2])
    now=datetime.now()
    secure_link_times="data_results/secure_link_"+platforms[platform_type]+"_2_salto_"+now.strftime("%m_%d_%Y_%H:%M:%S")+".dat"
    secure_link_timesht="data_results/secure_link_ht_"+platforms[platform_type]+"_2_salto_"+now.strftime("%m_%d_%Y_%H:%M:%S")+".dat"
    ciphertimerdifs=[]
    ciphertimerdifsht=[]
    rtimers=[]
    rtimersht=[]
    #global securetimeslink
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    for x in range(10):
        if x == 6:
            continue
        ###############compile images##################
        os.chdir(dir_path+"/contiki-ng/examples/coap/coap-example-client")
        compileimage(x,platform)
        if(platform_type==SENSORTAG):
            test_multihop_multiclient.sendaction('m-'+str(x))
        else:
            os.chdir(dir_path+"/contiki-ng/examples/coap/coap-example-server")
            compileimage(x,platform)
        os.chdir(dir_path)
        ###############run simulator##################
        timerdiffl=[]
        timerdifflht=[]
        rtimer=[]
        rtimerht=[]
        platform.run()
        for ren in range(10):
            ###############extract values from log files##################
            print("cifrador:",ciphers[x],"muestra:",ren)
            time.sleep(1)
            #----------------client----------------#
            clientuart=open(clientloguart,'r')
            lines=clientuart.readlines()
            clientuart.close()
            os.remove(clientloguart)
            for line in lines:
                if(line.find("inicio:")!=-1):
                    t1int=int(line[7:])
                    rtimer.append(t1int)
                if(line.find("htinit:")!=-1):
                    t1intht=int(line[7:])
                    rtimerht.append(t1intht)
                if(line.find("seguro:")!=-1):
                    t2int=int(line[7:])
                    rtimer.append(t2int)
                    timerdiffl.append(((t2int-t1int)/platform.segundo)*1000)
                if(line.find("htfin:")!=-1):
                    t2intht=int(line[6:])
                    rtimerht.append(t2intht)
                    timerdifflht.append(((t2intht-t1intht)/platform.segundo)*1000)
            #timerdiffl.append(random.randint(8,12))
            #timerdifflht.append(random.randint(8,12))
            #rtimer.append([100,110])
            #rtimerht.append([100,110])
                #else:
                #    print("fallo handshake")
            #-------------------------------------------------------------
            if(len(timerdiffl)==0):
                print("fallo el handshake")
            print(timerdiffl)
            print(rtimer)
            platform.run()
            #return
        #return
        ciphertimerdifs.append(timerdiffl)
        rtimers.append(rtimer)
        ciphertimerdifsht.append(timerdifflht)
        rtimersht.append(rtimerht)
    print(ciphertimerdifs)
    print(rtimers)
    print(ciphertimerdifsht)
    print(rtimersht)
    with open(secure_link_times,'w') as f:
        wr = csv.writer(f)
        wr.writerows(ciphertimerdifs)
    with open(secure_link_timesht,'w') as f:
        wr = csv.writer(f)
        wr.writerows(ciphertimerdifsht)
    #plotvellink(ciphertimerdifs,ciphertimerdifsht)



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
    plataform=renode.renode()
    os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test/coap-example-client")
    compileimage(GRAIN128,plataform,clean=1)
    os.chdir(dir_path+"/contiki-ng/examples/coap_cipher_vel_test/coap-example-server")
    compileimage(GRAIN128,plataform,clean=1)
    # plataform.run(1,1)
    # os.chdir(dir_path)
    #platform=cooja.cooja()
   
    #platform.run()
    #testimagessize(RENODE)
    #plotvelcipher(ciphertimerdifsencrypt,ciphertimerdifsdecrypt)
    pass
#dir_path = os.path.dirname(os.path.realpath(__file__))


