import math
import os
from time import sleep
import sys
import MySQLdb
import datetime
import subprocess
import random

os.system("git stash save --keep-index & disown")
sleep(5)
os.system("git pull origin master & disown")
#os.system("chmod -R 777 tools")
sleep(10)
os.system("rm nohup.out")
sleep(5)
print("Ready!!")
cmd=('nohup python3 by_album.py 20 4 200000 0</dev/null &')
os.system(cmd)
print(cmd)
sleep(5)
cmd=('nohup python3 by_search.py 20 7 20000 0</dev/null &')
os.system(cmd)
print(cmd)
sleep(5)
cmd=('nohup python3 by_search.py 20 7 20000 0</dev/null &')
os.system(cmd)
print(cmd)
sleep(5)
cmd=('nohup python3 by_search.py 20 7 20000 0</dev/null &')
os.system(cmd)
print(cmd)
sleep(5)
cmd=('nohup python3 by_search.py 20 7 20000 0</dev/null &')
os.system(cmd)
print(cmd)
sleep(5)
cmd=('nohup python3 by_search.py 20 7 20000 0</dev/null &')
os.system(cmd)
print(cmd)
sleep(5)
cmd=('nohup python3 by_search.py 20 7 20000 0</dev/null &')
os.system(cmd)
print(cmd)
sleep(5)
cmd=('nohup python3 by_save.py 20 7 20000 0</dev/null &')
os.system(cmd)
print(cmd)