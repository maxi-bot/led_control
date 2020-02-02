#!/bin/bash
apt update
apt upgrade -y
apt install pigpio apache2 python3
pip3 install websockets
rm pigpio.py
systemctl enable pigpiod
systemctl start pigpiod
IP=$(hostname -I)
IP=${IP%% *}
sed -i "s/localhost/$IP/g" html/script.js
cp html/* /var/www/html
service apache start
nohup python3 start.py