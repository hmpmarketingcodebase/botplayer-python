import os
from time import sleep
while(1):
    os.system('nohup sudo bash clean_tmp.sh 0</dev/null &')
    print("clear tmp file")
    sleep(5)
    print("clear cache RAM") 
    os.system('nohup sudo bash clean_ram.sh 0</dev/null &')
    sleep(5)
    os.system('nohup sudo killall chrome chromedriver 0</dev/null &')
    sleep(3600)