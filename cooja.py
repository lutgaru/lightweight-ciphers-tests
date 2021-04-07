import os

class cooja:
    segundo=1000000

    def make(self,defines='',with_clean=1):
        if with_clean==1:
            os.system("make TARGET=cooja clean")
        return os.system("make TARGET=cooja WERROR=0" +defines+ "MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")

    def run(self):
        pass