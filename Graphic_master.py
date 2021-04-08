import os
import subprocess
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import csv
import numpy as np
from telnetlib import Telnet

AES, GIFTCOFB, XOODYAK, ASCON128A, ASCON80, ASCON128, GRAIN128, TINYJAMBU192, TINYJAMBU256, TINYJAMBU128 = range(10)
ciphers=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' GRAIN128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']

def get_mean_error(data):
    mean=[]
    error=[]
    for dat in data:
        mean.append(np.mean(dat))
        error.append(np.std(dat))
    return (mean,error)

def graphic_data(data,name,namedata):
    datarray=[]
    meanarray=[]
    errorarray=[]
    bar_plots=[]
    x=list(range(10))
    for i,dat in enumerate(data):
        with open(dat,"r") as decv:
            read=csv.reader(decv)
            datarray.append([list(map(float,x)) for x in list(read)])
    #with open("data_results/securelinktiminght1_tag_3.dat","r") as decv:
    #    read=csv.reader(decv)
    #    securetimeslinkht=[list(map(float,x)) for x in list(read)]
        print(i)

        mean,error = get_mean_error(datarray[-1])
        meanarray.append(mean)
        errorarray.append(error)
        bar_plots.append(go.Bar(x=x,y=mean,name=namedata[i],error_y=dict(type='data',array=error)))
    #htmean,hterror = get_mean_error(securetimeslinkht)
    #bar_plots=[
    #    go.Bar(x=x,y=linkmean,name='Enlace Seguro', marker=dict(color='#0343df'),error_y=dict(type='data',array=linkerror)),
    #    go.Bar(x=x,y=htmean,name='Handshake', marker=dict(color='#e50000'),error_y=dict(type='data',array=hterror))
    #]


    layout=go.Layout(
        title=go.layout.Title(text=name, x=0.5),
        yaxis_title="ms",
        xaxis_tickmode="array",
        xaxis_tickvals=list(range(27)),
        xaxis_ticktext=ciphers,#tuple(df['year'].values),
    )

    # Make the multi-bar plot
    fig = go.Figure(data=bar_plots, layout=layout)

    # Tell Plotly to render it
    fig.show()

if __name__ == "__main__":
    file_list=[
        "data_results/securelinktiming1_tag_3.dat",
        "data_results/securelinktiminght1_tag_3.dat",
    ]
    namedata=[
        "Enlace seguro",
        "Handshake"
    ]
    graphic_data(file_list,"Enlace seguro 100 muestras sensortag",namedata)

    file_list=[
        "data_results/secure_link_Renode_1_salto_04_07_2021_20:47:53.dat",
        "data_results/secure_link_ht_Renode_1_salto_04_07_2021_20:47:53.dat",
    ]
    namedata=[
        "Enlace seguro",
        "Handshake"
    ]
    graphic_data(file_list,"Enlace seguro 5 muestras renode",namedata)
