#!/bin/bash
apt update
apt upgrade -y
apt install pigpio apache2 python3
pip3 install websockets
rm pigpio.py
systemctl enable pigpiod
cp html/* /var/www/html
service apache start