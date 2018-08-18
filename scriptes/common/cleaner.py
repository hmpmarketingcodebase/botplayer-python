import os
import subprocess
import psutil
from time import sleep
import datetime

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def clean_memory():
    now = datetime.datetime.now()
    if(int(now.hour) % 6 == 0 and int(now.minute) < 5):
       os.system('sudo bash clean_tmp.sh & disown')
       print("clear tmp file")
    sleep(5)

    if(int(now.hour) % 2 == 0 and int(now.minute) < 5):
       print("clear cache RAM") 
       os.system('sudo bash clean_ram.sh & disown')
         
    mem = psutil.virtual_memory()
    mem_ = sizeof_fmt(mem.free)
    print('Free memory :'+ str(mem_))
    if('MiB' in mem_):
      s = mem_[:-3]
      #print('memory use:'+ str(s))
      if(float(s) < 100 ):
         print("process killed")         
         os.system("killall chrome chromedriver")
         sleep(5)

while(1):
   clean_memory()
   print("# Cleaning")
   sleep(120)