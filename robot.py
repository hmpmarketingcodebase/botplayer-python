import math
import os
from time import sleep
import sys
import MySQLdb
import datetime
import subprocess
sys.path.insert(0, 'python_files/')
from heart import connectiondb


if(opsy=="linux"):
   os.system("killall python3 chrome chromedriver Xvfb")
   sleep(2)
   os.system("git stash save --keep-index & disown")
   sleep(5)
   os.system("git pull origin master & disown")
   sleep(20)
   os.system("chmod -R 777 shell")
   os.system("chmod -R 777 tools")
   sleep(10)
   print("Ready!!")



name=sys.argv[1]
behaivor=sys.argv[2]
number_threads=sys.argv[3]
country=sys.argv[4] 
id_playlist_album=sys.argv[5]    
id_playlist=sys.argv[6]
opsy=sys.argv[7]

   
if(opsy=="windows"):         
         cmd=('python robot.py ' + str(sys.argv[1]) + ' ' + str(sys.argv[2]) + ' ' + str(sys.argv[3]) +  ' ' + str(sys.argv[4]) + ' ' + str(sys.argv[5]) + ' ' + str(sys.argv[6]) + ' ' + str(sys.argv[7]) )
         subprocess.call(cmd, shell=True)
elif(opsy=="linux"):
         cmd=('python3 robot.py ' + str(sys.argv[1]) + ' ' + str(sys.argv[2]) + ' ' + str(sys.argv[3]) +  ' ' + str(sys.argv[4]) + ' ' + str(sys.argv[5]) + ' ' + str(sys.argv[6]) + ' ' + str(sys.argv[7]))
         subprocess.call(cmd, shell=True)
   