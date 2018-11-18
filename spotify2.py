import math
import os
from time import sleep
import sys
import MySQLdb
import datetime
import subprocess
import platform
sys.path.insert(0, 'scripts/spotify/')
import random
from requests import get
import psutil
import platform
sys.path.append(".")
import scriptes.common.heart

i=0

while(1):
   i+=1
   
   cmd=('nohup sudo bash clean_tmp.sh 0</dev/null &')
   subprocess.call(cmd, shell=True, cwd='scriptes/common/')
   sleep(3)


   cmd=('nohup sudo bash clean_ram.sh 0</dev/null &')
   subprocess.call(cmd, shell=True, cwd='scriptes/common/')
   sleep(3)

   if(i==1):
      cmd=('nohup python3 checker_proxies.py 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/common/')
      sleep(3)
  
      cmd=('nohup python3 load_proxies.py 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/common/')
      sleep(3)

      cmd=('nohup python3 by_album2.py 20 20 200000 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      sleep(3)

      cmd=('nohup python3 by_album2.py 20 20 200000 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      sleep(3)

      cmd=('nohup python3 by_album2.py 20 20 200000 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      sleep(3)

      cmd=('nohup python3 by_album2.py 20 20 200000 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      sleep(3)

      cmd=('nohup python3 by_album2.py 20 20 200000 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      sleep(3)

      cmd=('nohup python3 by_album2.py 20 20 200000 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      sleep(3)

      cmd=('nohup python3 by_album2.py 20 20 200000 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      sleep(3)

      cmd=('nohup python3 by_album2.py 20 20 200000 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      sleep(3)
   sleep(120)