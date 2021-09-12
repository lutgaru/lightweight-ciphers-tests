import matplotlib.pyplot as plt
import numpy as np
ciphers=['AES',' GIFTCOFB',' XOODYAK',' ASCON128A',' ASCON80',' ASCON128',' GRAIN128',' TINYJAMBU192',' TINYJAMBU256',' TINYJAMBU128','NOCIP']

filec='extralogs/batterycurrent500.dat'
filev='extralogs/batteryvoltage500.dat'
filec2='extralogs/batterycurrent5002.dat'
filev2='extralogs/batteryvoltage5002.dat'
filec3='extralogs/batterycurrent5003.dat'
filev3='extralogs/batteryvoltage5003.dat'

#filec='extralogs/batterycurrentlog2.dat'
#filev='extralogs/batteryvoltagelog2.dat'

with open(filec,'r') as f:
    current=f.readlines()

with open(filev,'r') as f:
    voltage=f.readlines()

with open(filec2,'r') as f:
    current2=f.readlines()

with open(filev2,'r') as f:
    voltage2=f.readlines()

with open(filec3,'r') as f:
    current3=f.readlines()

with open(filev3,'r') as f:
    voltage3=f.readlines()

currentvals=[float(x) for x in current[1:-1]]
currentvals2=[float(x) for x in current2[1:-1]]
currentvals3=[float(x) for x in current3[1:-1]]
# print(currentvals)

voltvals=[float(x) for x in (','.join(voltage[1:-1])).split(',')]
voltvals2=[float(x) for x in (','.join(voltage2[1:-1])).split(',')]
voltvals3=[float(x) for x in (','.join(voltage3[1:-1])).split(',')]
# print(voltage)

fig,axs=plt.subplots(1)
fig2,axs2=plt.subplots(1)

time=np.linspace(0, (len(voltvals)*100)/1000, len(voltvals))
timec=np.linspace(0, (len(voltvals)*100)/1000, len(currentvals))
time2=np.linspace(0, (len(voltvals2)*100)/1000, len(voltvals2))
timec2=np.linspace(0, (len(voltvals2)*100)/1000, len(currentvals2))

time3=np.linspace(0, (len(voltvals3)*100)/1000, len(voltvals3))
timec3=np.linspace(0, (len(voltvals3)*100)/1000, len(currentvals3))
axs.plot(time, voltvals)
axs.plot(time2, voltvals2)
axs.plot(time3, voltvals3)
#axs[0].plot(time2, voltvals2)
axs2.plot(timec,currentvals)
axs2.plot(timec2,currentvals2)
axs2.plot(timec3,currentvals3)
# axs.plot(timec2,currentvals2)
# axs.plot(timec3,currentvals3)
#fig[0].xlabel('Time (s)')
#plt.ylabel('Voltage (mV)')
plt.show()