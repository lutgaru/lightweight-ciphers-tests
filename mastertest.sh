#!/bin/zsh
dtlscontikidir="contiki-ng/os/net/security/tinydtls"
dtlslibcoapdir="libcoap/ext/tinydtls"
contikiexampledir="contiki-ng/examples/coap/coap-example-server"
libcoapdir="libcoap"
casa="${0:A:h}"

cd $dtlscontikidir
if [ -n "$(git diff --cached --exit-code)" ]; then
git commit --amend --author="lutgaru <lutgaru@gmail.com>" --no-edit 
fi
git push -f origin experimental_optim || exit_on_error "fallo el push"
cd $casa
echo "cd" $libcoap
cd $libcoapdir
git submodule update --remote
./autogen.sh
./configure --enable-dtls --with-tinydtls --disable-documentation
make clean
case "$1" in
    1)
        make MAKE_WITH_GIFTCOFB=1  NBYTES=3 && sudo make install #|| exit_on_error "fallo la instalacion de libcoap"
        ;;
    2)
        make MAKE_WITH_XOODYAK=1 && sudo make install #|| exit_on_error "fallo la instalacion de libcoap"
        ;;
    3)
        case "$2" in
        2)
            make MAKE_WITH_ASCON128A=1 && sudo make install #|| exit_on_error "fallo la instalacion de libcoap"
            ;;
        3)
            make MAKE_WITH_ASCON80=1 && sudo make install #|| exit_on_error "fallo la instalacion de libcoap"
            ;;
        *)
            make MAKE_WITH_ASCON128=1 && sudo make install #|| exit_on_error "fallo la instalacion de libcoap"
            ;;
        esac
        ;;
        
    4)
        make MAKE_WITH_GRAIN128=1 && sudo make install #|| exit_on_error "fallo la instalacion de libcoap"
        ;;
    5)
        case "$2" in
        2)
            make MAKE_WITH_TINYJAMBU192=1 && sudo make install #|| exit_on_error "fallo la instalacion de libcoap"
            ;;
        3)
            make MAKE_WITH_TINYJAMBU256=1 && sudo make install #|| exit_on_error "fallo la instalacion de libcoap"
            ;;
        *)
            make MAKE_WITH_TINYJAMBU128=1 && sudo make install #|| exit_on_error "fallo la instalacion de libcoap"
            ;;
        esac
        ;;
    *)
        make && sudo make install #|| exit_on_error "fallo la instalacion de libcoap"
        ;;
esac
cd $casa
cd $contikiexampledir
case "$1" in
    1)
        sudo ./test.sh 1
        ;;
    2)
        sudo ./test.sh 2
        ;;
    3)
        sudo ./test.sh 3 "$2"
        ;;
    4)
        sudo ./test.sh 4
        ;;
    5)
        sudo ./test.sh 5 "$2"
        ;;
    *)
        sudo ./test.sh
esac