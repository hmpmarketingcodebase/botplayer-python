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

try:
   mypubilcip = get('https://api.ipify.org').text
except:
   mypubilcip = "-"
   
#name of bot
name=sys.argv[1]
#start datetime
start_date=datetime.datetime.now()
#behivor id (from behaivor tabble)
behaivor=sys.argv[2]
#how many thread ?
number_threads=sys.argv[3]
#1 = run and 0 = stop
running = 1
#id playlist album
id_playlist_album=sys.argv[4]    
#id playlist
id_playlist=sys.argv[5]
#os (windows or linux)
opsy = platform.system() #operation system (windows or linux)
print("start")
#Connection
try:
    #cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.","spoti")    
    cnx = MySQLdb.connect("10.128.0.2","spoti","o85BIgDEfChf","spoti") 
    cursor = cnx.cursor()

    cmd="INSERT INTO `robot`(`name`, `start_date`, `behaivor`,`id_playlist`,`id_playlist_album`, `number_threads`, `running`, `country`) VALUES ('"+str(mypubilcip) + "', '"+str(start_date)+"', "+str(behaivor)+", "+str(id_playlist)+", "+str(id_playlist_album)+", "+str(number_threads)+", "+str(running)+", '-3')"
    print(cmd)
    cursor.execute(cmd)
    cnx.commit() 
except MySQLdb.Error as err:
    print("Something went wrong: {} ".format(err))


try:
    curs = cnx.cursor()
    curs.execute("select * from songs")
    songs = curs.fetchall()
    for s in songs:
        file = open("./scriptes/spotify/log/songs/"+str(s[0]),"w")        
except MySQLdb.Error as err:  
    print("Something went wrong: (song) {}".format(err)) 

i=0
arr = os.listdir('./scriptes/spotify/log/play')
for a in arr:
         scriptes.common.heart.read_log_update(a,cnx,'spoti','./scriptes/spotify/log/play/')
         sleep(1)
         cmd=('sudo rm '+str(a))
         subprocess.call(cmd, shell=True, cwd='scriptes/spotify/log/play')
         print(a)

print("Ready!!")
#get behaivor
try:
   cursor.execute("select * from behaivor where id = " + behaivor)  
   behaivor = cursor.fetchone() 
   behaivor_by_playlist=behaivor[2] # % 
   behaivor_by_artist=behaivor[3] # % 
   behaivor_by_album=behaivor[4] # %
   print("album " + str(behaivor_by_album))
   behaivor_by_search=behaivor[5] # %
   print("search " + str(behaivor_by_search))
   behaivor_by_direct_save=behaivor[6] # % 
   print("save " + str(behaivor_by_direct_save))
   behaivor_margin_play=behaivor[7] 
   min_play=behaivor[8] 
   max_play=behaivor[9] 
   number_of_server=behaivor[10] 
   
except MySQLdb.Error as err:  
   print("Something went wrong: (Behaivor) {}".format(err))   

t=int(random.randrange(min_play,max_play))
t=int(t/int(int(number_of_server) * int(number_threads)))
if(opsy=="Linux"):
   cmd=('rm nohup.out & disown')
   subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
   sleep(3)
   cmd=('nohup python3 cleaner.py 0</dev/null &')
   subprocess.call(cmd, shell=True, cwd='scriptes/common/')
   
sleep(5)
#run by playlist process
by_playlist=1
while(by_playlist <= int(behaivor_by_playlist)):
      if(opsy=="Windows"):          
         cmd=('start python by_playlist.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' + str(t))
      elif(opsy=="Linux"):
         cmd=('nohup  python3 by_playlist.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' '  + str(t) + ' 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      print(cmd)
      by_playlist = by_playlist + 1
      sleep(10)  

by_artist=1
while(by_artist <= int(behaivor_by_artist)):
      if(opsy=="Windows"):          
         cmd=('start python by_artist.py ' + str(t))
      elif(opsy=="Linux"):
         cmd=('nohup  python3 by_artist.py ' + str(t) + ' 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      print(cmd)
      by_artist = by_artist + 1
      sleep(10)  

#run by search process
by_search=1
while(by_search <= int(behaivor_by_search)):
      if(opsy=="Windows"):
         cmd=('start python by_search.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' +  str(t))
      elif(opsy=="Linux"): 
         cmd=('nohup  python3 by_search.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' +  str(t)+ ' 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      print(cmd)
      by_search = by_search + 1
      sleep(10)  

#run by direct save process
by_save=1
while(by_save <= int(behaivor_by_direct_save)):
      if(opsy=="Windows"):
         cmd=('start by_save.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' +  str(t) )
      elif(opsy=="Linux"):
         cmd=('nohup  python3 by_save.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' +  str(t) + ' 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      print(cmd)
      by_save = by_save + 1
      sleep(10)  

#run by album process
by_album=1
while(by_album <= int(behaivor_by_album)):
      if(opsy=="Windows"):
         cmd=('start python by_album.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist_album) + ' ' + str(t) )
      elif(opsy=="Linux"):
         cmd=('nohup  python3 by_album.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist_album) + ' ' + str(t)  + ' 0</dev/null &')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      print(cmd)
      by_album = by_album + 1
      sleep(10)