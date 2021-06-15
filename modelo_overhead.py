import matplotlib.pyplot as plt
import numpy as np
import math

# Data for plotting
Chunk=True
Fragment=True
fs=60
ncanales=2
bpm=16
overhead=[52,81,89,89,89,89,89,81,81,81]
overheadcipher=[0,8,16,16,16,16,16,8,8,8]
trugput=[]
empaquetado=range(1,60)
trbycip=[]
ciphers=['Sin cifrar','AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128','TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128']
nchunk=1
fig, ax = plt.subplots()
for i,over in enumerate(overhead):
    trugput=[]
    delay=[]
    for emp in empaquetado:
        nchunk=0
        carga=(bpm*ncanales*emp)
        if(carga>64*8) and Chunk:
            nchunk=math.ceil((carga)/(64*8))
        #if nchunk>1:
            #print("nc:",nchunk)
            trh=0
            for x in range(1,nchunk):
                #print(x)
                if Fragment:
                    sixcargaf=(((carga+(overheadcipher[i]+40)*8)-88*8)+28*8)
                    trh=trh+((125*8)*(fs/emp)+sixcargaf*(fs/emp))
                else:
                    trh=trh+((64*8+over*8)*(fs/emp))
                #print(trh)
            resto=carga-(64*8*(nchunk-1))
            if (resto>46*8) and Fragment:
                sixcargaf=(((resto+(overheadcipher[i]+40)*8)-88*8)+28*8)
                trh=trh+((125*8)*(fs/emp)+sixcargaf*(fs/emp))
            else:
                trh=trh+(((ncanales*bpm*emp)-(64*8*(nchunk-1)))+over*8)*(fs/emp)
            print(trh,ciphers[i])
            trugput.append(trh)
        else:
            if (carga>46*8) and Fragment:
                sixcargaf=(((carga+(overheadcipher[i]+40)*8)-88*8)+28*8)
                #trh=trh+((125)*(fs/emp)+sixcargaf*(fs/emp))
                trugput.append(((125*8)*(fs/emp)+sixcargaf*(fs/emp)))
            else:
                #trh=trh+(((ncanales*bpm*emp)-(64*8*(nchunk-1)))+over*8)*(fs/emp)
                trugput.append((carga+over*8)*(fs/emp))
            print("no chunk",trugput[-1],ciphers[i])
        delay.append(emp/fs)
    trbycip.append(trugput)
    #print(ciphers[i])
    ax.plot(empaquetado, trugput,label=ciphers[i])
    #ax.plot(empaquetado, delay)

ax.set(xlabel='Empaquetado de muestras ', ylabel='Velocidad en bps',
       title='Velocidad necesaria por nodo')
ax.grid()
ax.legend()

#fig.savefig("test.png")
plt.show()