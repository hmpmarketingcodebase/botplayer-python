import os
import subprocess
import psutil
from time import sleep

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