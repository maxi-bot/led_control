sudo apt update
sudo apt upgrade -y
sudo apt install pigpio apache2 python3
pip3 install websockets
rm pigpio.py
sudo systemctl enable pigpiod
cp html/* /var/www/html
sudo service apache start