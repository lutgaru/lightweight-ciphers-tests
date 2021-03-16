import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from telnetlib import Telnet
import time
import random
import csv

AES, GIFTCOFB, XOODYAK, ASCON128A, ASCON80, ASCON128, GRAIN128, TINYJAMBU192, TINYJAMBU256, TINYJAMBU128 = range(10)
sizesfilename='sizes_optim2.dat'
velencrypt='velencrypt2optim.dat'
veldecrypt='veldecrypt2optim.dat'
data_result_dir='/data_results'
coap_dir='/examples/coap'
clientloguart='clientloguart.dat'
serverloguart='serverloguart.dat'
ciphers=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' GRAIN128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']
textvs=[]
datavs=[]
bssvs=[]
decvs=[]
hexvs=[]
ciphertimerdifsdecrypt=[]
ciphertimerdifsencrypt=[]

def compileimage(typecif=AES):
    os.system("make TARGET=cc2538dk clean")
    if typecif==AES or typecif==GRAIN128:
        os.system("make TARGET=cc2538dk WERROR=0 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")
    elif typecif==GIFTCOFB:
        os.system("make TARGET=cc2538dk WERROR=0 MAKE_WITH_GIFTCOFB=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")
    elif typecif==XOODYAK:
        os.system("make TARGET=cc2538dk WERROR=0 MAKE_WITH_XOODYAK=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")
    elif typecif==ASCON128:
        os.system("make TARGET=cc2538dk WERROR=0 MAKE_WITH_ASCON128=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")
    elif typecif==ASCON128A:
        os.system("make TARGET=cc2538dk WERROR=0 MAKE_WITH_ASCON128A=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")
    elif typecif==ASCON80:
        os.system("make TARGET=cc2538dk WERROR=0 MAKE_WITH_ASCON80=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")
    #elif typecif==GRAIN128:
    #    os.system("make TARGET=cc2538dk WERROR=0 MAKE_WITH_GRAIN128=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")
    elif typecif==TINYJAMBU128:
        os.system("make TARGET=cc2538dk WERROR=0 MAKE_WITH_TINYJAMBU128=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")
    elif typecif==TINYJAMBU192:
        os.system("make TARGET=cc2538dk WERROR=0 MAKE_WITH_TINYJAMBU192=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")
    elif typecif==TINYJAMBU256:
        os.system("make TARGET=cc2538dk WERROR=0 MAKE_WITH_TINYJAMBU256=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")
    
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
                bar = ax.bar(x + x_offset, y,yerr=error[i][x], width=bar_width * single_width, color=colors[i % len(colors)],capsize=10)

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())   

def appendsize():
    sizestr=subprocess.run(["size","coap-example-client.cc2538dk"],stdout=subprocess.PIPE,text=True)
    sizesvals=sizestr.stdout.split("\n")[1].split("\t")
    print(sizestr.stdout.split("\n"))
    print(sizesvals)
    textvs.append(int(sizesvals[0]))
    datavs.append(int(sizesvals[1]))
    bssvs.append(int(sizesvals[2]))
    decvs.append(int(sizesvals[3]))
    #hexvs.append(int(sizesvals[4]))

def testimagessize():
    global textvs,datavs,bssvs,decvs,hexvs
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path+data_result_dir)
    if os.path.isfile(sizesfilename):
        sizesback = np.loadtxt(sizesfilename)
        textvs=sizesback[0,:]
        datavs=sizesback[1,:]
        bssvs=sizesback[2,:]
        decvs=sizesback[3,:]
        #hexvs=sizesback[4,:]
    else:
        os.chdir(dir_path+"contiki-ng/examples/coap/coap-example-client")
        for x in range(10):
            compileimage(x)
            appendsize()
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

def testvelocitycipher():
    global ciphertimerdifs
    global ciphertimerdifsdecrypt
    global ciphertimerdifsencrypt
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path+data_result_dir)
    if os.path.isfile(veldecrypt) and os.path.isfile(velencrypt):
        with open(veldecrypt,"r") as decv:
            read=csv.reader(decv)
            ciphertimerdifsdecrypt=[list(map(float,x)) for x in list(read)]
        with open(velencrypt,"r") as encv:
            read=csv.reader(encv)
            ciphertimerdifsencrypt=[list(map(float,x)) for x in list(read)]
        #velenback = np.load(velencrypt)
        #ciphertimerdifsencrypt=velenback.items()
        #velenback = np.load(veldecrypt)
        print(ciphertimerdifsdecrypt)
        print(ciphertimerdifsencrypt)
        #print(velenback)
        #ciphertimerdifsdecrypt=velenback.items()
        #hexvs=sizesback[4,:]
    else:
        for x in range(10):
            ###############compile images##################
            os.chdir(dir_path+"contiki-ng/examples/coap/coap-example-client")
            compileimage(x)
            os.chdir(dir_path+"contiki-ng/examples/coap/coap-example-server")
            compileimage(x)
            os.chdir(dir_path)
            ###############run renode emulator##################
            renode = subprocess.Popen(["renode", "--disable-xwt", "coap_test.resc", "--port", "33334"])
            print("Esperando..")
            time.sleep(120)
            tn = Telnet("127.0.0.1",33334)
            tn.write("quit\n".encode('ascii'))
            tn.close()
            if (renode.poll==None):
                renode.kill()
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
                    t1int=int(line[8:])
                if(line.find("decrypt2")!=-1):
                    t2int=int(line[8:])
                    timerdiffd.append(((t2int-t1int)/32768)*1000)
                if(line.find("encrypt1")!=-1):
                    t1int=int(line[8:])
                if(line.find("encrypt2")!=-1):
                    t2int=int(line[8:])
                    timerdiffe.append(((t2int-t1int)/32768)*1000)
            #----------------server----------------#
            serveruart=open(serverloguart,'r')
            lines=serveruart.readlines()
            serveruart.close
            os.remove(serverloguart)
            for line in lines:
                if(line.find("decrypt1")!=-1):
                    t1int=int(line[8:])
                if(line.find("decrypt2")!=-1):
                    t2int=int(line[8:])
                    timerdiffd.append(((t2int-t1int)/32768)*1000)
                if(line.find("encrypt1")!=-1):
                    t1int=int(line[8:])
                if(line.find("encrypt2")!=-1):
                    t2int=int(line[8:])
                    timerdiffe.append(((t2int-t1int)/32768)*1000)
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
    testvelocitycipher()
    #testimagessize()
    #plotvelcipher(ciphertimerdifsencrypt,ciphertimerdifsdecrypt)
    pass
#dir_path = os.path.dirname(os.path.realpath(__file__))


