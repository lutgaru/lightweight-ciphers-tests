trap "exit" INT TERM ERR
trap "kill 0" EXIT

compile()
{
make clean TARGET=cc2538dk
#make clean TARGET=cc26x0-cc13x0
case "$1" in
    1)
        make TARGET=cc2538dk WERROR=0 MAKE_WITH_GIFTCOFB=1 WITH_OPTIMIZATION=1  NBYTES=46 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
        ;;
    2)
        make TARGET=cc2538dk WERROR=0 MAKE_WITH_XOODYAK=1 WITH_OPTIMIZATION=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
        ;;
    3)
        case "$2" in
        2)
            make TARGET=cc2538dk WERROR=0 MAKE_WITH_ASCON128A=1 WITH_OPTIMIZATION=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
            ;;
        3)
            make TARGET=cc2538dk WERROR=0 MAKE_WITH_ASCON80=1 WITH_OPTIMIZATION=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
            ;;
        *)
            make TARGET=cc2538dk WERROR=0 MAKE_WITH_ASCON128=1 WITH_OPTIMIZATION=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
            ;;
        esac
        ;;
    4)
        make TARGET=cc2538dk WERROR=0 MAKE_WITH_GRAIN128=1 WITH_OPTIMIZATION=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
        ;;
    5)  
        case "$2" in
        2)
            make TARGET=cc2538dk WERROR=0 MAKE_WITH_TINYJAMBU192=1 WITH_OPTIMIZATION=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
            ;;
        3)
            make TARGET=cc2538dk WERROR=0 MAKE_WITH_TINYJAMBU256=1 WITH_OPTIMIZATION=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
            ;;
        *)
            make TARGET=cc2538dk WERROR=0 MAKE_WITH_TINYJAMBU128=1 WITH_OPTIMIZATION=1 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
            ;;
        esac
        ;;
    *)
        make TARGET=cc2538dk WERROR=0 MAKE_WITH_DTLS=1 WITH_OPTIMIZATION=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
        #make TARGET=cc26x0-cc13x0 BOARD=sensortag/cc2650 WERROR=0 MAKE_WITH_DTLS=1 MAKE_COAP_DTLS_KEYSTORE=MAKE_COAP_DTLS_KEYSTORE_SIMPLE
        ;;
esac
}
serverdir=contiki-ng/examples/coap_cipher_vel_test_final/coap-example-server
clientdir=contiki-ng/examples/coap_cipher_vel_test_final/coap-example-client
cd $clientdir
compile $1 $2 
cd ../../../../
cd $serverdir
compile $1 $2 
cd ../../../../

renode coap_test.resc