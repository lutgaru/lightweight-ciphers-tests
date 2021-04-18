import os
import docker
import subprocess

class cooja:
    segundo=1000000

    def make(self,defines='',with_clean=1,withoptim=1):
        if with_clean==1:
            os.system("make TARGET=cooja clean")
        return 0
        #return os.system("make TARGET=cooja WERROR=0" +defines+ "MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")

    def run(self,program=1,local=1,cipher=0):
        client=docker.from_env()
        container=client.containers.list()[0]
        output=container.exec_run('bash -c "cd tools/cooja && java -mx512m -jar dist/cooja.jar -nogui=../../prueba_2s_'+str(cipher)+'.csc"')
        # output=client.containers.run('contiker/contiki-ng',
        #     privileged=True,
        #     sysctls = { 'net.ipv6.conf.all.disable_ipv6': 0},
        #     mounts = [docker.types.Mount(type='bind',source='/home/nefta/lightweight-ciphers-tests/contiki-ng',target='/home/user/contiki-ng')],
        #     command='bash -c "cd tools/cooja && java -mx512m -jar dist/cooja.jar -nogui=../../prueba_1s_0.csc"',
        #     stream=True)
        #print(output[1].decode('utf-8'))

        clientloguartlines=[]
        with open('contiki-ng/tools/cooja/COOJA.testlog',"r") as decv:
                read=decv.readlines()
                for line in read:
                    linetemp=line.split(":")
                    if(len(linetemp)>2 and linetemp[1]=='1'):
                        newline=":".join(linetemp[2:])
                        #print(newline)
                        clientloguartlines.append(newline)
                    #print(line)
        with open('clientloguart.dat',"w") as decv:
            decv.writelines(clientloguartlines)
        pass

    def getsize(self):
        self.run()
        return subprocess.run(["size","coap-example-client.cooja"],stdout=subprocess.PIPE,text=True)
