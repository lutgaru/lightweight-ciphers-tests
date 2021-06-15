import socket
import sensortag
import main_tests
import asyncio
import websockets
import os
import time
import threading



async def ciphertest(websocket, path):
    platform=sensortag.sensortag()
    mesj = await websocket.recv()
    print("< {}".format(mesj))

    act=mesj.split('-')
    if act[0]=='m':
        main_tests.compileimage(int(act[1]),platform)
        greeting = "ok"
    if act[0]=='p':
        exito2=os.system("/opt/ti/uniflash/dslite.sh -c server.ccxml -f contiki-ng/examples/coap/coap-example-server/build/cc26x0-cc13x0/sensortag/cc2650/coap-example-server.hex")
        if (exito2!=0):
            greeting = "error"
        else:
            greeting = "ok"
    if act[0]=='r':
        ress="/opt/ti/uniflash/dslite.sh -c server.ccxml --post-flash-device-cmd PinReset"
        serverthread=threading.Thread(target=platform.threaduart,args=("/dev/ttyACM2","serverloguart.dat",45,ress,))#,daemon=True)
        print("= "*80)
        serverthread.start()
        print("Esperando")
        time.sleep(0.2)
        greeting="ok"
    await websocket.send(greeting)
    print("> {}".format(greeting))


def server():
    start_server = websockets.serve(ciphertest, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

async def saction(action):
    async with websockets.connect('ws://192.168.0.4:8765',ping_interval=None) as websocket:

        await websocket.send(action)
        print("> {}".format(action))

        greeting = await websocket.recv()
        print("< {}".format(greeting))
    #return(greeting)

def sendaction(action):
    return asyncio.get_event_loop().run_until_complete(saction(action))

if __name__ == "__main__":    
    server()
    pass
