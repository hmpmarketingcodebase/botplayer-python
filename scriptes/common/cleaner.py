import os
import subprocess
import psutil
from time import sleep

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def clean_memory():
    os.system('sudo bash clean_ram.sh & disown')
    sleep(5)
    os.system('sudo bash clean_tmp.sh & disown')
    sleep(5)
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