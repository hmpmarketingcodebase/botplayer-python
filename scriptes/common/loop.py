import os
while(1):
    os.system('sudo bash clean_tmp.sh & disown')
    print("clear tmp file")
    sleep(5)
    print("clear cache RAM") 
    os.system('sudo bash clean_ram.sh & disown')
    sleep(5)
    os.system('sudo killall chrome chromedriver')