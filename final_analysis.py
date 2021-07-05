from logging import error
import os
import subprocess
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from telnetlib import Telnet
import time
from datetime import datetime
from matplotlib.transforms import ScaledTranslation
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
ciphers=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']
ciphersst=['AES',' GIFTCOFB',' XOODYAK',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']
carpetas=['sensortagstdtesttable','sensortagstdtestconst','sensortag1s']

empaquetado=[1,6,9]
def graphic_vel_cipher(platform):
    timetest=600
    timecrypt=[]
    timedecrypt=[]
    fig,axs=plt.subplots()
    cmap = plt.get_cmap('tab10')
    colors = [cmap(i) for i in np.linspace(0, 1, 10)]
    #for i,cip in enumerate(ciphers):
    for i,pack in enumerate(empaquetado):
        timecryptp=[]
        timedecryptp=[]
        means=[]
        meansde=[]
        stds=[]
        stdsde=[]
        #for pack in empaquetado:
        for k,cip in enumerate(ciphers):
            with open('final_logs/renode/clientloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                for line in decv.readlines():
                    linesp=line.split(',')
                    if linesp[0]=='decrypt':
                        timedecryptp.append((1000*(int(linesp[2])-int(linesp[1])))/platform.segundo)
                    if linesp[0]=='encrypt':
                        timecryptp.append((1000*(int(linesp[2])-int(linesp[1])))/platform.segundo)
                
            with open('final_logs/renode/serverloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                for line in decv.readlines():
                    linesp=line.split(',')
                    if linesp[0]=='decrypt':
                        timedecryptp.append((1000*(int(linesp[2])-int(linesp[1])))/platform.segundo)
                    if linesp[0]=='encrypt':
                        timecryptp.append((1000*(int(linesp[2])-int(linesp[1])))/platform.segundo)
            means.append(np.mean(timecryptp[10:],axis=0))
            stds.append(np.std(timecryptp[10:],axis=0))
            meansde.append(np.mean(timedecryptp[10:],axis=0))
            stdsde.append(np.std(timedecryptp[10:],axis=0))
        #trans1 = axs.transData + ScaledTranslation(-5/72, 0, fig.dpi_scale_trans)
        #trans2 = axs.transData + ScaledTranslation(+5/72, 0, fig.dpi_scale_trans)
        axs.errorbar(ciphers,means,yerr=stds,fmt='v:',label=str(pack)+" crypt",color=colors[i], capsize=3, capthick=1)
        axs.errorbar(ciphers,meansde,yerr=stdsde,fmt='x:',label=str(pack)+" decrypt",color=colors[i], capsize=3, capthick=1)
        timedecrypt.append(timedecryptp)
        timecrypt.append(timecryptp)
    #print(timecrypt)
    #print(timedecrypt)
    
    plt.legend()
    axs.set_ylabel("ms")
    axs.set_xlabel("Muestra por paquetes")
    axs.set_title("Velcidad de cifrado y decifrado")
    plt.show()    

def graphic_vel_cipher_sensortag(platform):
    timetest=600
    timecrypt=[]
    timedecrypt=[]
    fig,axs=plt.subplots(3)
    cmap = plt.get_cmap('tab10')
    colors = [cmap(i) for i in np.linspace(0, 1, 10)]
    #for i,cip in enumerate(ciphers):
    for pl,carp in enumerate(carpetas):
        for i,pack in enumerate(empaquetado):
            timecryptp=[]
            timedecryptp=[]
            means=[]
            meansde=[]
            stds=[]
            stdsde=[]
            #for pack in empaquetado:
            for k,cip in enumerate(ciphersst):
                
                with open('final_logs/'+carp+'/clientloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                    inicio=False
                    for line in decv.readlines():
                        linesp=line.split(',')
                        #print(linesp)
                        if linesp[0]!='[INFO: CC26xx/CC13xx]  RF: Channel 26' and inicio==False:
                            #print(linesp)
                            continue
                        else:    
                            #print(linesp)  
                            inicio=True
                        if linesp[0]=='decrypt':
                            try:
                                time=(1000*(int(linesp[2])-int(linesp[1])))/platform.segundo
                                if (time)>=0:
                                    timedecryptp.append(time)
                            except:
                                print(linesp)
                        #if linesp[0]=='encrypt':
                        #    try:
                        #        timecryptp.append((1000*(int(linesp[2])-int(linesp[1])))/platform.segundo)
                        #    except:
                        #        print(decv.name)
                with open('final_logs/'+carp+'/serverloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                    inicio=False
                    for line in decv.readlines():
                        linesp=line.split(',')

                        if linesp[0]!='[INFO: CC26xx/CC13xx]  RF: Channel 26' and inicio==False:
                            continue
                        else:     
                            inicio=True
                        #if linesp[0]=='decrypt':
                        #    timedecryptp.append((1000*(int(linesp[2])-int(linesp[1])))/platform.segundo)
                        if linesp[0]=='encrypt':
                            try:
                                time=(1000*(int(linesp[2])-int(linesp[1])))/platform.segundo
                                if (time)>=0:
                                    timecryptp.append(time)
                            except:
                                print(linesp)
                means.append(np.mean(timecryptp[20:],axis=0))
                stds.append(np.std(timecryptp[20:],axis=0))
                meansde.append(np.mean(timedecryptp[20:],axis=0))
                stdsde.append(np.std(timedecryptp[20:],axis=0))
            #trans1 = axs.transData + ScaledTranslation(-5/72, 0, fig.dpi_scale_trans)
            #trans2 = axs.transData + ScaledTranslation(+5/72, 0, fig.dpi_scale_trans)
            axs[pl].errorbar(ciphersst,means,yerr=stds,fmt='v:',label=str(pack)+" crypt",color=colors[i], capsize=3, capthick=1)
            axs[pl].errorbar(ciphersst,meansde,yerr=stdsde,fmt='x:',label=str(pack)+" decrypt",color=colors[i], capsize=3, capthick=1)
            axs[pl].legend()
            axs[pl].set_ylabel("ms")
            axs[pl].set_xlabel("Muestra por paquetes")
            axs[pl].set_title("Velcidad de cifrado y decifrado "+carp)
            timedecrypt.append(timedecryptp)
            timecrypt.append(timecryptp)
    #print(timecrypt)
    #print(timedecrypt)
    
    #plt.legend()
    #axs.set_ylabel("ms")
    #axs.set_xlabel("Muestra por paquetes")
    #axs.set_title("Velcidad de cifrado y decifrado")
    plt.show()          

#platform=renode.renode()
platform=sensortag.sensortag()
graphic_vel_cipher_sensortag(platform)