#!/bin/zsh

cd contiki-ng/examples/libs/timers
#make TARGET=cc2538dk clean
make TARGET=cc2538dk
cd ../../../../
../renode/renode tsch_test.resc
