#!/bin/bash

sudo tar -czf rcv.tar.gz --exclude=".git" --exclude="*.mp4" --exclude="*.avi" --exclude="__pycache__" --exclude="*.pyc" -C ${1}  rcv
scp rcv.tar.gz pi@${2}:~
sudo rm -f rcv.tar.gz
ssh pi@${2} 'sudo rm /var/log/daemon.log'
ssh pi@${2} 'sudo systemctl stop rcv.service'
ssh pi@${2} 'sudo rm -rf rcv'
ssh pi@${2} 'sudo tar -xzf rcv.tar.gz'
ssh pi@${2} 'sudo rm -f rcv.tar.gz'
ssh pi@${2} 'sudo rcv/install.sh'
ssh pi@${2} 'sudo systemctl daemon-reload'
ssh pi@${2} 'sudo systemctl start rcv.service'
