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
import plotly
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

def to_miliseconds(rtimerv):
    return (rtimerv/platform.segundo)*1000

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

def extract_power(list,list2):
    times=[]
    for i in range(len(list)-1):
        pwr=(((6.1*10**-3)*3.3)*((int(list[i+1])-int(list[i]))/1000))
        pwt=(((6.1*10**-3)*3.3)*((int(list2[i+1])-int(list2[i]))/1000))
        times.append(pwr+pwt)
    #print(times,list)
    return times

def extract_energy():
    timetest=600
    carp=carpetas[6]
    fig,axs=plt.subplots(1)
    grapenergy=make_subplots(rows=4, cols=1,subplot_titles=['Cliente','Oxímetro','Termómetro','Baumanómetro'])
    for i,pack in enumerate(empaquetado):
            clientcpus=[]
            clientlpms=[]
            clientdeplpms=[]
            clienttotalcpus=[]
            clientlistens=[]
            clienttransmits=[]
            clientrtotals=[]
            oximlistens=[]
            oximtransmits=[]
            templistens=[]
            temptransmits=[]
            presslistens=[]
            presstransmits=[]
            #for pack in empaquetado:
            for k,cip in enumerate(ciphersst):
                clientcpu=[]
                clientlpm=[]
                clientdeplpm=[]
                clienttotalcpu=[]
                clientlisten=[]
                clienttransmit=[]
                oximlisten=[]
                oximtransmit=[]
                clientrtotal=[]
                templisten=[]
                temptransmit=[]
                presslisten=[]
                presstransmit=[]
                with open('final_logs/'+carp+'/clientloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                     clientlines=decv.readlines()
                with open('final_logs/'+carp+'/oximloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                     oximlines=decv.readlines()
                with open('final_logs/'+carp+'/temploguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                     templines=decv.readlines()
                with open('final_logs/'+carp+'/presloguart_'+cip+'_'+str(pack)+'_'+str(timetest)+'.dat',"r", errors='ignore') as decv:
                     presslines=decv.readlines()
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
                inicio=False
                for oximline in oximlines:
                    linea=oximline.split(',')
                    if linea[0]!='[INFO: CC26xx/CC13xx]  RF: Channel 26' and inicio==False:
                            #print(linesp)
                            continue
                    inicio=True 
                    if linea[0]=='ER':
                        oximlisten.append(int(linea[1]))
                        oximtransmit.append(int(linea[2]))
                inicio=False
                for pressline in presslines:
                    linea=pressline.split(',')
                    if linea[0]!='[INFO: CC26xx/CC13xx]  RF: Channel 26' and inicio==False:
                            #print(linesp)
                            continue
                    inicio=True 
                    if linea[0]=='ER':
                        presslisten.append(int(linea[1]))
                        presstransmit.append(int(linea[2]))
                inicio=False
                for templine in templines:
                    linea=templine.split(',')
                    if linea[0]!='[INFO: CC26xx/CC13xx]  RF: Channel 26' and inicio==False:
                            #print(linesp)
                            continue
                    inicio=True 
                    if linea[0]=='ER':
                        templisten.append(int(linea[1]))
                        temptransmit.append(int(linea[2]))
                        #clientrtotal.append(int(linea[3]))
                        #print(linea)
                #print(clientlpm)
                clientcpus.append(clientcpu)
                clientlpms.append(clientlpm)
                clientdeplpms.append(clientdeplpm)
                clienttotalcpus.append(clienttotalcpu)
                clientlistens.append(clientlisten)
                clienttransmits.append(clienttransmit)
                clientrtotals.append(clientrtotal)
                oximlistens.append(oximlisten)
                oximtransmits.append(oximtransmit)
                templistens.append(templisten)
                temptransmits.append(temptransmit)
                presslistens.append(presslisten)
                presstransmits.append(presstransmit)
                #print(clienttotalcpu)
            #print([np.std(extract_power(x)) for x in clienttotalcpus])
            #axs.errorbar(ciphersst,[np.mean(extract_power(x)) for x in clientlistens],yerr=[np.std(extract_power(x)) for x in clientlistens],fmt='v:',label=str(pack)+" listen", capsize=3, capthick=1)
            #axs.errorbar(np.linspace(0,10,len(clientlistens[0])),clientlistens[0],fmt='v:',label=str(pack)+" listen", capsize=3, capthick=1)
            #axs.errorbar(ciphersst,[np.mean(extract_power(clientlistens[idd],clienttransmits[idd])) for idd,x in enumerate(clienttotalcpus)],yerr=[np.std(extract_power(x)) for x in clienttotalcpus],fmt='*:',label=str(pack)+" totalcpu", capsize=3, capthick=1)
            #axs.errorbar(ciphersst,[np.mean(extract_power(x)) for x in clienttransmits],yerr=[np.std(extract_power(x)) for x in clienttransmits],fmt='.:',label=str(pack)+" transmit", capsize=3, capthick=1)
            #print(oximtransmits)
            grapenergy.add_trace(go.Bar(y=[np.mean(extract_power(clientlistens[idd],clienttransmits[idd])) for idd,x in enumerate(clienttotalcpus)],x=ciphersst,name=packet[i],marker_color=plotly.colors.qualitative.Plotly[i],error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=[np.std(extract_power(clientlistens[idd],clienttransmits[idd])) for idd,x in enumerate(clienttotalcpus)],
            visible=True),),1,1)
            grapenergy.add_trace(go.Bar(y=[np.mean(extract_power(oximlistens[idd],oximtransmits[idd])) for idd,x in enumerate(oximtransmits)],x=ciphersst,name=packet[i],marker_color=plotly.colors.qualitative.Plotly[i],error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=[np.std(extract_power(oximlistens[idd],oximtransmits[idd])) for idd,x in enumerate(oximtransmits)],
            visible=True),showlegend=False),2,1)
            grapenergy.add_trace(go.Bar(y=[np.mean(extract_power(presslistens[idd],presstransmits[idd])) for idd,x in enumerate(presstransmits)],x=ciphersst,name=packet[i],marker_color=plotly.colors.qualitative.Plotly[i],error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=[np.std(extract_power(presslistens[idd],presstransmits[idd])) for idd,x in enumerate(presstransmits)],
            visible=True),showlegend=False),3,1)
            grapenergy.add_trace(go.Bar(y=[np.mean(extract_power(templistens[idd],temptransmits[idd])) for idd,x in enumerate(temptransmits)],x=ciphersst,name=packet[i],marker_color=plotly.colors.qualitative.Plotly[i],error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=[np.std(extract_power(templistens[idd],temptransmits[idd])) for idd,x in enumerate(temptransmits)],
            visible=True),showlegend=False),4,1)
            #axs.errorbar(ciphersst,[np.mean(extract_power(x)) for x in clientrtotals],yerr=[np.std(extract_power(x)) for x in clientrtotals],fmt='v:',label=str(pack)+" rtotals", capsize=3, capthick=1)
            #exit()
    plt.legend()
    grapenergy.update_yaxes(title_text="Watts",range=[0.02012,0.02016],row=1,col=1)
    grapenergy.update_yaxes(title_text="Watts",range=[0.02012,0.02016],row=2,col=1)
    grapenergy.update_yaxes(title_text="Watts",range=[0.02012,0.02016],row=3,col=1)
    grapenergy.update_yaxes(title_text="Watts",range=[0.02012,0.02016],row=4,col=1)
    grapenergy.show()
    grapenergy.write_image("/home/arts1/Documents/graficasalv/"+"powercons"+carp+".pdf",width=1000,height=720)
    #plt.show()
            #print(clienttransmits)

def extract_times():
    timetest=600
    carp=carpetas[6]
    medias=[]
    jitters=[]
    graphtimes=go.Figure()
    tiemposfc=[]
    tiemprosc=[]
    tempdelayc=[]
    presdelayc=[]
    for k,cip in enumerate(ciphersst[:]):
        fig = go.Figure()
        difdel=go.Figure()
        media=[]
        jitter=[]
        tiemposfp=[]
        tiemprosp=[]
        tempdelayp=[]
        presdelayp=[]
        #for pack in empaquetado:
        for iem,pack in enumerate(empaquetado[:]):
            times=go.Figure()
            T_0s=[]
            T_0ds=[]
            T_1s=[]
            tiempros=[]
            tempdelay=[]
            presdelay=[]
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
                        if len(linea)<5:
                            tiempros.append(int(linea[3])-int(linea[2]))
                        else:
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
            tiemprosp.append(tiempros)
            timedif1=[]
            timedif2=[]
            for clientline in clientlines:
                        clinea=clientline.split(',')
                        if clinea[0]!='[INFO: CC26xx/CC13xx]  RF: Channel 26' and inicio2==False:
                                continue
                        inicio2=True
                        if clinea[0].find('|t') !=-1:
                            
                            #print(clinea[3][:-2],clinea[3][:-1])
                            print(clinea)
                            try:
                               tempdelay.append(int(clinea[2])-int(clinea[1]))
                               print(clinea)
                            except:
                                pass
                            #break
                        if clinea[0]=='|':
                            #print(clinea[3][:-2],clinea[3][:-1])
                            print(clinea)
                            try:
                               presdelay.append(int(clinea[2])-int(clinea[1]))
                            except:
                                pass
                            #break
            tempdelayp.append(tempdelay)
            presdelayp.append(presdelay)
            for itime in range(len(T_1s)-1):
                timedif1.append((T_0s[itime]-T_0s[itime+1])-(T_1s[itime]-T_1s[itime+1]))
                timedif2.append((T_0s[itime]-T_1s[itime]))
                #timedif.append(T_0s[itime]-T_0s[itime+1])
            #print(T_1s)
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

            #print(T_0s)
   
        #difdel.add_trace(go.Scatter(y=media,x=cip))
        tiemposfc.append(tiemposfp)
        tiemprosc.append(tiemprosp)
        tempdelayc.append(tempdelayp)
        presdelayc.append(presdelayp)
        #fig.show()
        #difdel.show()
    with open('data_extracted/'+carp+'.pkl','wb') as f:
        pickle.dump(tiemposfc,f)
    with open('data_extracted/'+carp+'pros.pkl','wb') as f:
        pickle.dump(tiemprosc,f)
    with open('data_extracted/'+carp+'temppress.pkl','wb') as f:
        pickle.dump([tempdelayc,presdelayc],f)
    #difdel.add_trace(go.Scatter(medias))
    #difdel.show()
            

def analizedata():
    file=carpetas[6]
    timeposfc=[]
    with open('data_extracted/'+file+'.pkl','rb') as f:
        timeposfc=pickle.load(f)
    with open('data_extracted/'+file+'pros.pkl','rb') as f:
        tiemprosc=pickle.load(f)
    with open('data_extracted/'+file+'temppress.pkl','rb') as f:
        tempdelayc,presdelayc=pickle.load(f)
    #print(tempdelayc,presdelayc)
    #print(tiemprosc)
    mastergrap=go.Figure()
    mastergrapjitt=go.Figure()
    mastergraptemp=go.Figure()
    mastergrappros=go.Figure()
    meanc=[]
    stdc=[]
    meand1c=[]
    stdd1c=[]
    meantc=[]
    stdtc=[]
    meanprc=[]
    stdprc=[]
    for cidd,timeposfp in enumerate(timeposfc[:]):
        difdel=go.Figure()
        dif1grap=go.Figure()
        tempgraph=go.Figure()
        prosgraph=go.Figure()
        meanp=[]
        stdp=[]
        meand1p=[]
        stdd1p=[]
        meantp=[]
        stdtp=[]
        meanprp=[]
        stdprp=[]
        for iddpos,timepos in enumerate(timeposfp):
            timedif2=[]
            timedif1=[]
            T_0s,T_1s=timepos
            #print(len(T_1s))
            for itime in range(len(T_1s)-1):
                resta=T_0s[itime]-T_1s[itime]
                if -100000<resta<100000:
                    timedif2.append(to_miliseconds(T_0s[itime]-T_1s[itime]))
                #if abs((T_0s[itime]-T_0s[itime+1])-(T_1s[itime]-T_1s[itime+1]))<100000:
                #    timedif1.append(abs((T_0s[itime]-T_0s[itime+1])-(T_1s[itime]-T_1s[itime+1])))
                if abs((T_0s[itime+1]-T_1s[itime+1])-(T_0s[itime]-T_1s[itime]))<100000:
                    timedif1.append(abs(to_miliseconds(T_0s[itime+1]-T_1s[itime+1])-(T_0s[itime]-T_1s[itime])/(len(T_0s)-1)))
            if min(timedif2)<0:
                for i,dif2 in enumerate(timedif2):
                    timedif2[i]=dif2-min(timedif2)
                    
            meanp.append(np.mean(timedif2))
            stdp.append(np.std(timedif2))
            meand1p.append(np.mean(timedif1))
            stdd1p.append(np.std(timedif1))
            difdel.add_trace(go.Scatter(x=np.linspace(0,10,len(timedif2)),y=timedif2))
            dif1grap.add_trace(go.Scatter(x=np.linspace(0,10,len(timedif2)),y=timedif1))
            #print(tiemprosc[cidd])
            prosgraph.add_trace(go.Scatter(x=np.linspace(0,10,len(tiemprosc[cidd][iddpos])),y=tiemprosc[cidd][iddpos]))
            tempgraph.add_trace(go.Scatter(x=np.linspace(0,10,len([z for z in tempdelayc[cidd][iddpos] if z<20000])),y=[z for z in tempdelayc[cidd][iddpos] if z<20000]))
            meantp.append(to_miliseconds(np.mean([z for z in tempdelayc[cidd][iddpos] if z<20000])))
            stdtp.append(to_miliseconds(np.std([z for z in tempdelayc[cidd][iddpos] if z<10000])))
            meanprp.append(to_miliseconds(np.mean([z for z in tiemprosc[cidd][iddpos] if -2000<z<2000])))
            stdprp.append(to_miliseconds(np.std([z for z in tiemprosc[cidd][iddpos] if -2000<z<2000])))
        meanc.append(meanp)
        stdc.append(stdp)
        meantc.append(meantp)
        stdtc.append(stdtp)
        meand1c.append(meand1p)
        stdd1c.append(stdd1p)
        meanprc.append(meanprp)
        stdprc.append(stdprp)
        difdel.update_layout(title=ciphersst[cidd])
        #difdel.show()
        dif1grap.update_layout(title=ciphersst[cidd])
        #dif1grap.show()
        tempgraph.update_layout(title=ciphersst[cidd])
        #prosgraph.show()
        #tempgraph.show()
    means=np.array(meanc).T.tolist()
    #print(meanc)
    #print(means)
    stds=np.array(stdc).T.tolist()
    meansd1=np.array(meand1c).T.tolist()
    stdsd1=np.array(stdd1c).T.tolist()
    meanst=np.array(meantc).T.tolist()
    stdst=np.array(stdtc).T.tolist()
    meanspr=np.array(meanprc).T.tolist()
    stdspr=np.array(stdprc).T.tolist()
    for idd,m in enumerate(means):
        mastergrap.add_trace(go.Bar(y=m,x=ciphersst,name=packet[idd],error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=stds[idd],
            visible=True)))
        mastergrapjitt.add_trace(go.Bar(y=meansd1[idd],x=ciphersst,name=packet[idd],error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=stdsd1[idd],
            visible=True)))
        mastergraptemp.add_trace(go.Bar(y=meanst[idd],x=ciphersst,name=packet[idd],error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=stdst[idd],
            visible=True)))
        mastergrappros.add_trace(go.Bar(y=meanspr[idd],x=ciphersst,name=packet[idd],error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=stdspr[idd],
            visible=True)))
    mastergrap.update_layout(yaxis_title="ms",)
    mastergrap.show()
    #mastergrap.write_image("/home/arts1/Documents/graficasalv/"+"Endtoenddelayestimado"+file+".pdf",width=1000,height=720)
    mastergrapjitt.update_layout(yaxis_title="ms",)
    mastergrapjitt.show()
    #mastergrapjitt.write_image("/home/arts1/Documents/graficasalv/"+"Jitterpromedio"+file+".pdf",width=1000,height=720)
    mastergraptemp.update_layout(yaxis_title="ms",)
    mastergraptemp.show()
    #mastergraptemp.write_image("/home/arts1/Documents/graficasalv/"+"latenciasolicitud-respuesta"+file+".pdf",width=1000,height=720)
    mastergrappros.update_layout(yaxis_title="ms",)
    mastergrappros.show()
    mastergrappros.write_image("/home/arts1/Documents/graficasalv/"+"proccesstime"+file+".pdf",width=1000,height=720)

platform=renode.renode()
#platform=sensortag.sensortag()
#graphic_vel_cipher_sensortag(platform)
#analizedata()
extract_energy()
#extract_times()