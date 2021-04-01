import os

class cooja:
    segundo=1000000

    def make(self,defines='',with_clean=1):
        return os.system("make TARGET=cc2538dk WERROR=0" +defines+ "MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE")

    def run(self):
        pass