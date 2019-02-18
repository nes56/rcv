#!/bin/sh

#disabling rcv.service (to not try and start the service on boot)
sudo systemctl disable rcv.service

#removing the rcv service 
sudo rm -f /lib/systemd/system/rcv.service

#removing the symbolic link from /opt if exists
if [ -L "/opt/rcv" ]; then
    sudo rm -f /opt/rcv
fi
