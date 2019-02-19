#!/bin/bash

CHECKOUT_DIR='/home/pi/rcv'

# create /opt/rcv link to the code
if [ ! -L "/opt/rcv" ]; then
    sudo ln -s ${CHECKOUT_DIR} /opt
fi

# install service file
sudo ln -s /opt/rcv/service/rcv.service /lib/systemd/system/rcv.service
if [ ! -d "${CHECKOUT_DIR}/logs" ]; then
    echo "mkdir ${CHECKOUT_DIR}/logs ....."
    mkdir "${CHECKOUT_DIR}/logs"
fi
# enabling the rcv.service
sudo systemctl  enable rcv.service

