import os
import subprocess
import matplotlib.pyplot as plt
import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import csv
import numpy as np
from telnetlib import Telnet

AES, GIFTCOFB, XOODYAK, ASCON128A, ASCON80, ASCON128, GRAIN128, TINYJAMBU192, TINYJAMBU256, TINYJAMBU128 = range(10)
ciphers=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' GRAIN128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']
ciphers2=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']
ciphers3=['AES',' GIFTCOFB',' XOODYAK',' GRAIN128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']

def get_mean_error(data):
    mean=[]
    error=[]
    for dat in data:
        mean.append(np.mean(dat))
        error.append(np.std(dat))
    return (mean,error)

def graphic_data_subplot(data,name,namedata,xtitles=ciphers2,ranges=[[[],[]],[[],[]]]):
    bar_plots=[]
    x=list(range(10))

    for i,dat in enumerate(data):
        datarray=[]
        meanarray=[]
        errorarray=[]
        for files in dat:
            with open(files,"r") as decv:
                read=csv.reader(decv)
                templist=[list(map(float,x)) for x in list(read)]
                
                if len(datarray)==0:
                    for dataitem in templist:
                        datarray.append(dataitem)
                else:
                    for di,dataitem in enumerate(datarray):
                        dataitem=dataitem+templist[di]
                        datarray[di]=dataitem

        mean,error = get_mean_error(datarray)
        meanarray.append(mean)
        errorarray.append(error)
        #print(len(errorarray),len(meanarray))
        bar_plots.append(go.Bar(x=xtitles,y=mean,name=namedata[i],text=mean,textposition="outside",texttemplate='%{value:.3f}',error_y=dict(type='data',array=error)))
    #htmean,hterror = get_mean_error(securetimeslinkht)
    #bar_plots=[
    #    go.Bar(x=x,y=linkmean,name='Enlace Seguro', marker=dict(color='#0343df'),error_y=dict(type='data',array=linkerror)),
    #    go.Bar(x=x,y=htmean,name='Handshake', marker=dict(color='#e50000'),error_y=dict(type='data',array=hterror))
    #]

    layout=go.Layout(
        #title=go.layout.Title(text=namedata[0], x=0.5),
        yaxis_title="ms",
        yaxis=dict(
                range=ranges[0]
            ),
        yaxis2=dict(
                range=ranges[1]
            ),
        xaxis_tickmode="array",
        xaxis_tickvals=list(range(27)),
        #xaxis_ticktext=ciphers2,#tuple(df['year'].values),
    )

    # Make the multi-bar plot
    #fig = go.Figure(data=bar_plots, layout=layout)
    fig = make_subplots(rows=len(bar_plots), cols=1, subplot_titles=["Enlace Seguro","Handshake"])

    for nbar,bar in enumerate(bar_plots): 
        fig.add_trace(bar,row=nbar+1,col=1)
        fig.update_yaxes(title_text="ms", row=nbar+1, col=1)
        #fig.update_xaxes(xaxis_ticktext=ciphers2,row=nbar+1, col=1)
    # Tell Plotly to render it
    fig.update_layout(layout)
    fig.show()
    fig.write_image("/home/nefta/tesismaster/trabajossecundarios/avance2/graficas/"+name+".pdf",
    width=1000,height=720)

def graphic_data(data,name,namedata,xtitles=ciphers2,ranges=[[],[]]):
    
    x=list(range(10))
    bar_plots=[]
    for i,dat in enumerate(data):
        datarray=[]
        meanarray=[]
        errorarray=[]
        for files in dat:
            with open(files,"r") as decv:
                read=csv.reader(decv)
                templist=[list(map(float,x)) for x in list(read)]
                
                if len(datarray)==0:
                    for dataitem in templist:
                        datarray.append(dataitem)
                else:
                    for di,dataitem in enumerate(datarray):
                        dataitem=dataitem+templist[di]
                        datarray[di]=dataitem
                        #print(templist[di])
                        #print(dataitem)
                #print(len(templist), templist[0])
                #print(len(datarray), datarray[0])
    #with open("data_results/securelinktiminght1_tag_3.dat","r") as decv:
    #    read=csv.reader(decv)
    #    securetimeslinkht=[list(map(float,x)) for x in list(read)]
        #print(i)
        #print(datarray[-1])
        mean,error = get_mean_error(datarray)
        meanarray.append(mean)
        errorarray.append(error)
        bar_plots.append(go.Bar(x=x,y=mean,name=namedata[i],text=mean,texttemplate='%{value:.3f}',textposition="outside",error_y=dict(type='data',array=error)))
    #htmean,hterror = get_mean_error(securetimeslinkht)
    #bar_plots=[
    #    go.Bar(x=x,y=linkmean,name='Enlace Seguro', marker=dict(color='#0343df'),error_y=dict(type='data',array=linkerror)),
    #    go.Bar(x=x,y=htmean,name='Handshake', marker=dict(color='#e50000'),error_y=dict(type='data',array=hterror))
    #]


    layout=go.Layout(
        title=go.layout.Title(text=name, x=0.5),
        yaxis_title="ms",
        yaxis=dict(
                range=ranges
            ),
        xaxis_tickmode="array",
        xaxis_tickvals=list(range(27)),
        xaxis_ticktext=xtitles,#tuple(df['year'].values),
    )

    # Make the multi-bar plot
    fig = go.Figure(data=bar_plots, layout=layout)

    # Tell Plotly to render it
    fig.show()
    fig.write_image("/home/nefta/tesismaster/trabajossecundarios/avance2/graficas/"+name+".pdf",
    width=1000,height=380)

def plot_size_image(file,title):
    sizesback = np.loadtxt(file)
    textvs=sizesback[0,:]
    datavs=sizesback[1,:]
    bssvs=sizesback[2,:]
    decvs=sizesback[3,:]
    barplots=[]
    print(textvs)
    romusage=textvs+datavs
    ramusage=datavs+bssvs
    barplots.append(go.Bar(x=ciphers,y=ramusage,name="RAM"))
    barplots.append(go.Bar(x=ciphers,y=romusage,name="ROM"))
    # Make the multi-bar plot
    layout=go.Layout(
        title=go.layout.Title(text=title, x=0.5),
        yaxis_title="Bytes",
        xaxis_tickmode="array",
        xaxis_tickvals=list(range(27)),
        #xaxis_ticktext=xtitles,#tuple(df['year'].values),
    )

    fig = go.Figure(data=barplots, layout=layout)

    # Tell Plotly to render it
    fig.show()

def plot_size_image_subplot(files,title,platforms,ranges):
    
    barplotsd=[]
    fig = make_subplots(rows=2, cols=1, subplot_titles=["Uso de RAM","Uso de ROM"])
    clors=px.colors.qualitative.D3#['#E74C3C','#2E86C1']
    for filei,file in enumerate(files):
        sizesback = np.loadtxt(file)
        textvs=sizesback[0,:]
        datavs=sizesback[1,:]
        bssvs=sizesback[2,:]
        decvs=sizesback[3,:]
        barplots=[]
        print(textvs)
        romusage=textvs+datavs
        ramusage=datavs+bssvs

        barplots.append(go.Bar(x=ciphers,y=ramusage,text=ramusage,textposition='auto',name=platforms[filei],marker_color=clors[filei]))
        barplots.append(go.Bar(x=ciphers,y=romusage,text=romusage,textposition='auto',name=platforms[filei],marker_color=clors[filei]))
        # Make the multi-bar plot
        layout=go.Layout(
            #title=go.layout.Title(text=title, x=0.5),
            yaxis_title="Bytes",
            yaxis=dict(
                range=ranges[0]
            ),
            yaxis2=dict(
                range=ranges[1]
            ),
            xaxis_tickmode="array",
            xaxis_tickvals=list(range(27)),
            #colorway=px.colors.qualitative.D3
            #xaxis_ticktext=xtitles,#tuple(df['year'].values),
        )

    

        for nbar,bar in enumerate(barplots): 
            #bar.marker.color=['#2874A6']
            # fig.add_shape(type="line",
            # x0=-1, y0=32000, x1=len(ciphers), y1=32000,
            # line=dict(
            #     color="LightSeaGreen",
            #     width=4,
            #     dash="dashdot",
            #     )
            # )
            fig.add_trace(bar,row=nbar+1,col=1)
            fig.update_yaxes(title_text="Bytes", row=nbar+1, col=1)
        #fig.update_xaxes(xaxis_ticktext=ciphers2,row=nbar+1, col=1)
    # Tell Plotly to render it
    
    fig.update_layout(layout)
    fig.show()
    #fig.write_image("/home/nefta/tesismaster/trabajossecundarios/avance2/graficas/"+title+".pdf",
    #width=1000,height=720)


if __name__ == "__main__":

    #plot_size_image_subplot("data_results/sizes_optim2.dat","Tamaño de las imagenes para cc2538")
    #plot_size_image_subplot("data_results/sizes_optim.dat","Tamaño de las imagenes para cc2538")
    # ranges=[[16500, 17500],[50000, 130000]]
    # plot_size_image_subplot(["data_results/sizes_Renode_04_14_2021_22:03:15.dat",
    #                         #"data_results/sizes_Cooja_04_14_2021_21:52:41.dat",
    #                         "data_results/sizes_Sensortag_04_14_2021_21:59:49.dat"],
    #                         "Tamaño de las imagenes optimizadas para cc2538 (Renode) y Sensortag cc2650",
    #                         ["Renode","Sensortag"],ranges)
    # ranges=[[16500, 100000],[50000, 350000]]
    # plot_size_image_subplot(["data_results/sizes_Cooja_04_14_2021_21:52:41.dat"],"Tamaño de las imagenes para cooja",["Cooja"],ranges)
    ##plot_size_image_subplot(["data_results/sizes_Sensortag_04_14_2021_21:59:49.dat"],"Tamaño de las imagenes optimizadas para Sensortag",["Sensortag"])


    # file_list=[
    #     ["data_results/veldecryptpruebaRenode04_15_2021_16:04:57.dat",],
    #     ["data_results/velencryptpruebaRenode04_15_2021_16:04:57.dat",]
    # ]
    # namedata=[
    #     "Descencriptar",
    #     "Encriptar"
    # ]
    # graphic_data(file_list,"Velocidad Optimizado cc2538(Renode)",namedata,ciphers)

    file_list=[
        ["data_results/veldecryptpruebaSensortag04_15_2021_17:13:12.dat",],
        ["data_results/velencryptpruebaSensortag04_15_2021_17:13:12.dat",]
    ]
    namedata=[
        "Descencriptar",
        "Encriptar"
    ]
    graphic_data(file_list,"Velocidad Optimizado cc2650(Sensortag)",namedata,ciphers,ranges=[1,2])

    # file_list=[
    #     ["data_results/veldecryptpruebaSensortag04_16_2021_00:52:37.dat",],
    #     ["data_results/velencryptpruebaSensortag04_16_2021_00:52:37.dat",]
    # ]
    # namedata=[
    #     "Descencriptar",
    #     "Encriptar"
    # ]
    # graphic_data(file_list,"Velocidad cc2650(Sensortag)",namedata,ciphers3)

    # file_list=[
    #     ["data_results/veldecryptpruebaRenode04_15_2021_22:46:08.dat",],
    #     ["data_results/velencryptpruebaRenode04_15_2021_22:46:08.dat",]
    # ]
    # namedata=[
    #     "Descencriptar",
    #     "Encriptar"
    # ]
    # graphic_data(file_list,"Velocidad cc2538(Renode)",namedata,ciphers)

    


    # file_list=[
    #     ["data_results/securelinktiming1_tag_3.dat",],
    #     ["data_results/securelinktiminght1_tag_3.dat",]
    # ]
    # namedata=[
    #     "Enlace seguro",
    #     "Handshake"
    # ]
    # graphic_data(file_list,"Enlace seguro 100 muestras sensortag 1 salto",namedata,ciphers)
    # graphic_data_subplot(file_list,"Enlace seguro 100 muestras sensortag 1 salto",namedata,ciphers)

    # file_list=[
    #     ["data_results/secure_link_Renode_1_salto_04_07_2021_20:47:53.dat",],
    #     ["data_results/secure_link_ht_Renode_1_salto_04_07_2021_20:47:53.dat",]
    # ]
    # namedata=[
    #     "Enlace seguro",
    #     "Handshake"
    # ]
    # graphic_data(file_list,"Enlace seguro 5 muestras renode 1 salto",namedata,ciphers)
    # graphic_data_subplot(file_list,"Enlace seguro 5 muestras renode 1 salto",namedata,ciphers)

    file_list=[
        ["data_results/secure_link_Cooja_1_salto_04_14_2021_23:53:33.dat",
        "data_results/secure_link_Cooja_1_salto_04_15_2021_00:04:08.dat",
        "data_results/secure_link_Cooja_1_salto_04_15_2021_00:14:43.dat"],
        ["data_results/secure_link_ht_Cooja_1_salto_04_14_2021_23:53:33.dat",
        "data_results/secure_link_ht_Cooja_1_salto_04_15_2021_00:04:08.dat",
        "data_results/secure_link_ht_Cooja_1_salto_04_15_2021_00:14:43.dat"]
    ]
    namedata=[
        "Enlace seguro",
        "Handshake"
    ]
    #graphic_data(file_list,"Enlace seguro 10 muestras cooja 1 salto",namedata)
    graphic_data_subplot(file_list,"Enlace seguro 100 muestras cooja 1 salto",namedata,ranges=[[14539,14541],[281,282]])

    file_list=[
        ["data_results/secure_link_Cooja_2_salto_04_15_2021_00:47:24.dat",
        "data_results/secure_link_Cooja_2_salto_04_15_2021_00:58:25.dat",
        "data_results/secure_link_Cooja_2_salto_04_15_2021_01:09:29.dat"],
        ["data_results/secure_link_ht_Cooja_2_salto_04_15_2021_00:47:24.dat",
        "data_results/secure_link_ht_Cooja_2_salto_04_15_2021_00:58:25.dat",
        "data_results/secure_link_ht_Cooja_2_salto_04_15_2021_01:09:29.dat"]
    ]
    namedata=[
        "Enlace seguro",
        "Handshake"
    ]
    #graphic_data(file_list,"Enlace seguro 10 muestras cooja 2 salto",namedata)
    graphic_data_subplot(file_list,"Enlace seguro 100 muestras cooja 2 saltos",namedata,ranges=[[29907,29908],[670,675]])

    file_list=[
        ["data_results/secure_link_Renode_1_salto_04_07_2021_20:47:53.dat",
        ],
        ["data_results/secure_link_ht_Renode_1_salto_04_07_2021_20:47:53.dat",
        ]
    ]
    namedata=[
        "Enlace seguro",
        "Handshake"
    ]
    #graphic_data(file_list,"Enlace seguro 10x10 muestras sensortag 2 saltos",namedata)
    graphic_data_subplot(file_list,"Enlace seguro 1x10 muestras renode 1 salto",namedata,xtitles=ciphers,ranges=[[4100,4105],[38,43]])

    file_list=[
        ["data_results/secure_link_Renode_2_salto_04_15_2021_01:26:34.dat",
        "data_results/secure_link_Renode_2_salto_04_15_2021_02:45:45.dat",
        "data_results/secure_link_Renode_2_salto_04_15_2021_04:04:57.dat",
        "data_results/secure_link_Renode_2_salto_04_15_2021_05:24:09.dat",
        "data_results/secure_link_Renode_2_salto_04_15_2021_06:43:21.dat",
        "data_results/secure_link_Renode_2_salto_04_15_2021_08:02:34.dat",
        "data_results/secure_link_Renode_2_salto_04_15_2021_09:21:47.dat",
        "data_results/secure_link_Renode_2_salto_04_15_2021_10:40:59.dat",
        "data_results/secure_link_Renode_2_salto_04_15_2021_12:00:13.dat",
        "data_results/secure_link_Renode_2_salto_04_15_2021_13:19:25.dat"
        ],
        ["data_results/secure_link_ht_Renode_2_salto_04_15_2021_01:26:34.dat",
        "data_results/secure_link_ht_Renode_2_salto_04_15_2021_02:45:45.dat",
        "data_results/secure_link_ht_Renode_2_salto_04_15_2021_04:04:57.dat",
        "data_results/secure_link_ht_Renode_2_salto_04_15_2021_05:24:09.dat",
        "data_results/secure_link_ht_Renode_2_salto_04_15_2021_06:43:21.dat",
        "data_results/secure_link_ht_Renode_2_salto_04_15_2021_08:02:34.dat",
        "data_results/secure_link_ht_Renode_2_salto_04_15_2021_09:21:47.dat",
        "data_results/secure_link_ht_Renode_2_salto_04_15_2021_10:40:59.dat",
        "data_results/secure_link_ht_Renode_2_salto_04_15_2021_12:00:13.dat",
        "data_results/secure_link_ht_Renode_2_salto_04_15_2021_13:19:25.dat"
        ]
    ]
    namedata=[
        "Enlace seguro",
        "Handshake"
    ]
    #graphic_data(file_list,"Enlace seguro 10x10 muestras sensortag 2 saltos",namedata)
    graphic_data_subplot(file_list,"Enlace seguro 10x10 muestras renode 2 saltos",namedata,xtitles=ciphers,ranges=[[8288,8295],[42,47]])


    file_list=[
        ["data_results/securelinktiming1_tag_3.dat",
        ],
        ["data_results/securelinktiminght1_tag_3.dat",
        ]
    ]
    namedata=[
        "Enlace seguro",
        "Handshake"
    ]
    #graphic_data(file_list,"Enlace seguro 10x10 muestras sensortag 2 saltos",namedata)
    graphic_data_subplot(file_list,"Enlace seguro 10x10 muestras sensortag 1 saltos",namedata,ranges=[[10000,20000],[300,610]])

    file_list=[
        ["data_results/secure_link_Sensortag_2_salto_04_13_2021_12:54:29.dat",
        "data_results/secure_link_Sensortag_2_salto_04_13_2021_14:26:00.dat",
        "data_results/secure_link_Sensortag_2_salto_04_13_2021_15:57:35.dat",
        "data_results/secure_link_Sensortag_2_salto_04_13_2021_17:29:14.dat",
        "data_results/secure_link_Sensortag_2_salto_04_13_2021_19:00:55.dat",
        "data_results/secure_link_Sensortag_2_salto_04_13_2021_20:32:39.dat",
        "data_results/secure_link_Sensortag_2_salto_04_13_2021_22:04:21.dat",
        "data_results/secure_link_Sensortag_2_salto_04_13_2021_23:36:11.dat",
        "data_results/secure_link_Sensortag_2_salto_04_14_2021_01:08:14.dat",
        "data_results/secure_link_Sensortag_2_salto_04_14_2021_02:40:07.dat"
        ],
        ["data_results/secure_link_ht_Sensortag_2_salto_04_13_2021_12:54:29.dat",
        "data_results/secure_link_ht_Sensortag_2_salto_04_13_2021_14:26:00.dat",
        "data_results/secure_link_ht_Sensortag_2_salto_04_13_2021_15:57:35.dat",
        "data_results/secure_link_ht_Sensortag_2_salto_04_13_2021_17:29:14.dat",
        "data_results/secure_link_ht_Sensortag_2_salto_04_13_2021_19:00:55.dat",
        "data_results/secure_link_ht_Sensortag_2_salto_04_13_2021_20:32:39.dat",
        "data_results/secure_link_ht_Sensortag_2_salto_04_13_2021_22:04:21.dat",
        "data_results/secure_link_ht_Sensortag_2_salto_04_13_2021_23:36:11.dat",
        "data_results/secure_link_ht_Sensortag_2_salto_04_14_2021_01:08:14.dat",
        "data_results/secure_link_ht_Sensortag_2_salto_04_14_2021_02:40:07.dat"
        ]
    ]
    namedata=[
        "Enlace seguro",
        "Handshake"
    ]
    #graphic_data(file_list,"Enlace seguro 10x10 muestras sensortag 2 saltos",namedata)
    graphic_data_subplot(file_list,"Enlace seguro 10x10 muestras sensortag 2 saltos",namedata,ranges=[[20000,33000],[600,1500]])


    # file_list=[
    #     ["data_results/secure_link_Renode_2_salto_04_15_2021_01:26:34.dat",],
    #     ["data_results/secure_link_ht_Renode_2_salto_04_15_2021_01:26:34.dat",]
    # ]
    # namedata=[
    #     "Enlace seguro",
    #     "Handshake"
    # ]
    # graphic_data(file_list,"Enlace seguro 10 muestras Rendoe 2 salto",namedata)
    # graphic_data_subplot(file_list,"Enlace seguro 10 muestras Renode 2 salto",namedata)

