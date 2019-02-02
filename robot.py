import os 
from time import sleep
import datetime
import subprocess
import sys
   
if(sys.argv[7]=="windows"):         
   cmd=('python robot.py ' + str(sys.argv[1]) + ' ' + str(sys.argv[2]) + ' ' + str(sys.argv[3]) +  ' ' + str(sys.argv[4]) + ' ' + str(sys.argv[5]) + ' ' + str(sys.argv[6]) + ' ' + str(sys.argv[7]) )
   subprocess.call(cmd, shell=True)
elif(sys.argv[7]=="linux"):
   os.system("git stash save --keep-index & disown")
   sleep(5)
   os.system("git pull origin master & disown")
   sleep(20)
   os.system("chmod -R 777 tools")
   sleep(10)
   print("Ready!!!")

   cmd=('python3 spotify.py ' + str(sys.argv[1]) + ' ' + str(sys.argv[2]) + ' ' + str(sys.argv[3]) +  ' ' + str(sys.argv[4]) + ' ' + str(sys.argv[5]) + ' ' + str(sys.argv[6]) + ' ' + str(sys.argv[7]))
   subprocess.call(cmd, shell=True)
   