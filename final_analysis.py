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

from numpy.core.fromnumeric import mean, std
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
import pickle

from telnetlib import Telnet
AES, GIFTCOFB, XOODYAK, ASCON128A, ASCON80, ASCON128, GRAIN128, TINYJAMBU192, TINYJAMBU256, TINYJAMBU128 = range(10)
ciphers=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']
ciphersst=['AES',' GIFTCOFB',' XOODYAK',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128','NOCIP']
packet=['1 Muestra','6 Muestras','9 Muestras']
carpetas=['sensortagstdtesttable','sensortagstdtestconst','sensortag1s','escenariomultisalto','escenario1malla','escenariomultisalto2','escenario2malla2','escenariomultisalto30min']

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

def extract_power(list):
    times=[]
    for i in range(len(list)-1):
        times.append(int(list[i+1])-int(list[i]))
    #print(times,list)
    return times

def extract_energy():
    timetest=600
    carp=carpetas[6]
    fig,axs=plt.subplots(1)
    for i,pack in enumerate(empaquetado):
            clientcpus=[]
            clientlpms=[]
            clientdeplpms=[]
            clienttotalcpus=[]
            clientlistens=[]
            clienttransmits=[]
            clientrtotals=[]
            #for pack in empaquetado:
            for k,cip in enumerate(ciphersst):
                clientcpu=[]
                clientlpm=[]
                clientdeplpm=[]
                clienttotalcpu=[]
                clientlisten=[]
                clienttransmit=[]
                clientrtotal=[]
                with open('final_logs/'+carp+'/clientloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                     clientlines=decv.readlines()
                with open('final_logs/'+carp+'/clientloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                     oximlines=decv.readlines()
                inicio=False
                for clientline in clientlines:
                    linea=clientline.split(',')
                    if linea[0]!='[INFO: CC26xx/CC13xx]  RF: Channel 26' and inicio==False:
                            #print(linesp)
                            continue
                    inicio=True
                    if linea[0]=='EC':
                        clientcpu.append(int(linea[1]))
                        clientlpm.append(int(linea[2]))
                        clientdeplpm.append(int(linea[3]))
                        clienttotalcpu.append(int(linea[4]))
                        #print(linea)
                    if linea[0]=='ER':
                        clientlisten.append(int(linea[1]))
                        clienttransmit.append(int(linea[2]))
                        clientrtotal.append(int(linea[3]))
                        #print(linea)
                #print(clientlpm)
                clientcpus.append(clientcpu)
                clientlpms.append(clientlpm)
                clientdeplpms.append(clientdeplpm)
                clienttotalcpus.append(clienttotalcpu)
                clientlistens.append(clientlisten)
                clienttransmits.append(clienttransmit)
                clientrtotals.append(clientrtotal)
                #print(clienttotalcpu)
            print([np.std(extract_power(x)) for x in clienttotalcpus])
            axs.errorbar(ciphersst,[np.mean(extract_power(x)) for x in clientlistens],yerr=[np.std(extract_power(x)) for x in clientlistens],fmt='v:',label=str(pack)+" listen", capsize=3, capthick=1)
            #axs.errorbar(np.linspace(0,10,len(clientlistens[0])),clientlistens[0],fmt='v:',label=str(pack)+" listen", capsize=3, capthick=1)
            #axs.errorbar(ciphersst,[np.mean(extract_power(x)) for x in clienttotalcpus],yerr=[np.std(extract_power(x)) for x in clienttotalcpus],fmt='*:',label=str(pack)+" totalcpu", capsize=3, capthick=1)
            axs.errorbar(ciphersst,[np.mean(extract_power(x)) for x in clienttransmits],yerr=[np.std(extract_power(x)) for x in clienttransmits],fmt='.:',label=str(pack)+" transmit", capsize=3, capthick=1)
            #axs.errorbar(ciphersst,[np.mean(extract_power(x)) for x in clientrtotals],yerr=[np.std(extract_power(x)) for x in clientrtotals],fmt='v:',label=str(pack)+" rtotals", capsize=3, capthick=1)
            #exit()
    plt.legend()
    plt.show()
            #print(clienttransmits)

def extract_times():
    timetest=1800
    carp=carpetas[7]
    medias=[]
    jitters=[]
    graphtimes=go.Figure()
    tiemposfc=[]
    for k,cip in enumerate(ciphersst[1:]):
        fig = go.Figure()
        difdel=go.Figure()
        media=[]
        jitter=[]
        tiemposfp=[]
        #for pack in empaquetado:
        for iem,pack in enumerate(empaquetado[:]):
            times=go.Figure()
            T_0s=[]
            T_0ds=[]
            T_1s=[]
            tiempros=[]
            with open('final_logs/'+carp+'/clientloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                    clientlines=decv.readlines()
            with open('final_logs/'+carp+'/oximloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                    oximlines=decv.readlines()
            inicio=False
            #print(clientlines[0])
            try:
                timeclient=datetime.strptime(clientlines[0],'TT,%m,%d,%y,%H,%M,%S,%f\n')
                timeoxim=datetime.strptime(oximlines[0],'TT,%m,%d,%y,%H,%M,%S,%f\n') 
                delta=timeclient-timeoxim
                deltartimer=((delta.total_seconds()*1000000)*platform.segundo)/1000000
            except:
                deltartimer=0
            
            #print(delta.total_seconds()*1000000,deltartimer)
            for oximline in oximlines:
                linea=oximline.split(',')
                if linea[0]!='[INFO: CC26xx/CC13xx]  RF: Channel 26' and inicio==False:
                        continue
                inicio=True
                #print(linea)
                if linea[0]=='o':
                    tempT1=linea[2]
                    try:
                        tiempros.append(int(linea[5])-int(linea[2]))
                    except:
                        pass
                    inicio2=False
                    for clientline in clientlines:
                        clinea=clientline.split(',')
                        if clinea[0]!='[INFO: CC26xx/CC13xx]  RF: Channel 26' and inicio2==False:
                                continue
                        inicio2=True
                        if clinea[0]=='o' and clinea[2]==linea[1]:
                            
                            #print(clinea[3][:-2],clinea[3][:-1])
                            try:
                                T_0s.append(int(clinea[3]))
                                T_0ds.append(int(clinea[3])-deltartimer)
                                T_1s.append(int(tempT1))
                            except:
                                pass
                            # if(T_0s[-1]<T_1s[-1]):
                            #     print(clinea,T_0s[-1])
                            #     print(oximline,T_1s[-1])
                            break
            tiemposfp.append([T_0s,T_1s])        
            
            timedif1=[]
            timedif2=[]
            for itime in range(len(T_1s)-1):
                timedif1.append((T_0s[itime]-T_0s[itime+1])-(T_1s[itime]-T_1s[itime+1]))
                timedif2.append((T_0s[itime]-T_1s[itime]))
                #timedif.append(T_0s[itime]-T_0s[itime+1])
            print(T_1s)
            #axs.plot(timedif1)
            times.add_trace(go.Scatter(x=np.linspace(0,10,len(T_1s)),y=T_1s))
            times.add_trace(go.Scatter(x=np.linspace(0,10,len(T_0s)),y=T_0s))
            times.add_trace(go.Scatter(x=np.linspace(0,10,len(T_0ds)),y=T_0ds))
            fig.add_trace(go.Scatter(x=np.linspace(0,10,len(tiempros)),y=tiempros))
            difdel.add_trace(go.Scatter(x=np.linspace(0,10,len(timedif2)),y=timedif2))
            media.append(np.mean(timedif2))
            jitter.append(np.std(timedif2))
            #axs.plot(T_1s)
            #axs.plot(T_0s)
            #axs.plot(timedif1)
            #times.show()

            print(T_0s)
   
        #difdel.add_trace(go.Scatter(y=media,x=cip))
        tiemposfc.append(tiemposfp)
        fig.show()
        difdel.show()
    with open('data_extracted/'+carp+'.pkl','wb') as f:
        pickle.dump(tiemposfc,f)
    #difdel.add_trace(go.Scatter(medias))
    #difdel.show()
            

def analizedata():
    file=carpetas[5]
    timeposfc=[]
    with open('data_extracted/'+file+'.pkl','rb') as f:
        timeposfc=pickle.load(f)
    mastergrap=go.Figure()
    mastergrapjitt=go.Figure()
    meanc=[]
    stdc=[]
    meand1c=[]
    stdd1c=[]
    for cidd,timeposfp in enumerate(timeposfc[:]):
        difdel=go.Figure()
        dif1grap=go.Figure()
        meanp=[]
        stdp=[]
        meand1p=[]
        stdd1p=[]
        for timepos in timeposfp:
            timedif2=[]
            timedif1=[]
            T_0s,T_1s=timepos
            #print(len(T_1s))
            for itime in range(len(T_1s)-1):
                resta=T_0s[itime]-T_1s[itime]
                if -100000<resta<100000:
                    timedif2.append((T_0s[itime]-T_1s[itime]))
                if abs((T_0s[itime]-T_0s[itime+1])-(T_1s[itime]-T_1s[itime+1]))<100000:
                    timedif1.append(abs((T_0s[itime]-T_0s[itime+1])-(T_1s[itime]-T_1s[itime+1])))
            if min(timedif2)<0:
                for i,dif2 in enumerate(timedif2):
                    timedif2[i]=dif2-min(timedif2)
                    
            meanp.append(np.mean(timedif2))
            stdp.append(np.std(timedif2))
            meand1p.append(np.mean(timedif1))
            stdd1p.append(np.std(timedif1))
            difdel.add_trace(go.Scatter(x=np.linspace(0,10,len(timedif2)),y=timedif2))
            dif1grap.add_trace(go.Scatter(x=np.linspace(0,10,len(timedif2)),y=timedif1))
        meanc.append(meanp)
        stdc.append(stdp)
        meand1c.append(meand1p)
        stdd1c.append(stdd1p)
        difdel.update_layout(title=ciphersst[cidd])
        #difdel.show()
        dif1grap.update_layout(title=ciphersst[cidd])
        #dif1grap.show()
    means=np.array(meanc).T.tolist()
    #print(meanc)
    #print(means)
    stds=np.array(stdc).T.tolist()
    meansd1=np.array(meand1c).T.tolist()
    stdsd1=np.array(stdd1c).T.tolist()
    for idd,m in enumerate(means):
        mastergrap.add_trace(go.Scatter(y=m,x=ciphersst,name=packet[idd],error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=stds[idd],
            visible=True)))
        mastergrapjitt.add_trace(go.Scatter(y=meansd1[idd],x=ciphersst,name=packet[idd],error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=stdsd1[idd],
            visible=True)))
    mastergrap.show()
    mastergrapjitt.show()

platform=renode.renode()
#platform=sensortag.sensortag()
#graphic_vel_cipher_sensortag(platform)
analizedata()
#extract_energy()
#extract_times()