#!/bin/bash -x
# @script       run.sh
# @author       Anthony Vilarim Caliani
# @contact      github.com/avcaliani
#
# @description
# Script to execute Spark Shell jobs...
#
# @usage
# ./run.sh
spark-shell -I main.scala \
    && rm -f data/*.txt data/avocado/*.crc \
    && mv data/avocado/*.txt data/AVOCADO.TXT \
    && rm -rf data/avocado \
    && exit 0
