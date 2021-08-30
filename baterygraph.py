import matplotlib.pyplot as plt
import numpy as np
ciphers=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' GRAIN128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128','NOCIP']

filec='extralogs/batterycurrentlogst'+ciphers[10]+'9.dat'
filev='extralogs/batteryvoltagelogst'+''+ciphers[10]+'9.dat'

with open(filec,'r') as f:
    current=f.readlines()

with open(filev,'r') as f:
    voltage=f.readlines()

currentvals=[float(x) for x in current[1:-1]]
print(currentvals)

voltvals=[float(x) for x in (','.join(voltage[1:-1])).split(',')]
print(voltage)

fig,axs=plt.subplots(2)

time=np.linspace(0, (len(voltvals)*100)/1000, len(voltvals))
timec=np.linspace(0, (len(voltvals)*100)/1000, len(currentvals))
axs[0].plot(time, voltvals)
axs[1].plot(timec,currentvals)
#fig[0].xlabel('Time (s)')
#plt.ylabel('Voltage (mV)')
plt.show()