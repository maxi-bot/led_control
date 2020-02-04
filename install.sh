#!/bin/bash
apt install pigpio nginx python3
pip3 install websockets
rm pigpio.py
systemctl enable pigpiod
systemctl start pigpiod
IP=$(hostname -I)
IP=${IP%% *}
sed -i "s/localhost/$IP/g" html/script.js
cp html/* /var/www/html
service nginx start
nohup python3 start.py &
