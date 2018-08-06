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

#name of bot
name=sys.argv[1]
#start datetime
start_date=datetime.datetime.now()
#behivor id (from behaivor tabble)
behaivor=sys.argv[2]
#how many thread ?
number_threads=8
#1 = run and 0 = stop
running = 1
#id playlist album
id_playlist_album=sys.argv[4]    
#id playlist
id_playlist=sys.argv[5]
#os (windows or linux)
opsy = platform.system() #operation system (windows or linux)

#Connection
try:
  #cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.","spoti")
  cnx = MySQLdb.connect("10.128.0.2","spoti","o85BIgDEfChf","spoti") 
  cursor = cnx.cursor()
except MySQLdb.Error as err:
  print("Error connection")

#insert robot datas 
try:
    cmd="INSERT INTO `robot`(`name`, `start_date`, `behaivor`,`id_playlist`,`id_playlist_album`, `number_threads`, `running`, `country`) VALUES ('"+str(name) + "', '"+str(start_date)+"', "+str(behaivor)+", "+str(id_playlist)+", "+str(id_playlist_album)+", "+str(number_threads)+", "+str(running)+", '0')"
    cursor.execute(cmd)
    cnx.commit() 
except MySQLdb.Error as err:
    print("Something went wrong: {}".format(err))


#reset in use account
try:
    cmd="update account set in_use = '0'"
    cursor.execute(cmd)
    cnx.commit() 
except MySQLdb.Error as err:
    print("Something went wrong: {}".format(err))

i=0
if(opsy=="Linux"):
    os.system("git config --global user.email 'zzakariaa10@yahoo.fr' & disown")
    sleep(5)
    os.system("git config --global user.email 'git config --global user.name 'Zak'")
    sleep(5)
    os.system("git stash save --keep-index & disown")
    sleep(5)
    os.system("git pull origin master & disown")
    #os.system("chmod -R 777 tools")
    sleep(10)
    os.system("rm nohup.out")
    sleep(5)
print("Ready!!")
#get behaivor
try:
   cursor.execute("select * from behaivor where id = " + behaivor)  
   behaivor = cursor.fetchone() 
   behaivor_by_playlist=behaivor[2] # % 
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
#run by playlist process
by_playlist=1
while(by_playlist <= int(behaivor_by_playlist)):
      if(opsy=="Windows"):          
         cmd=('start python by_playlist.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' + str(t))
      elif(opsy=="Linux"):
         cmd=('python3 by_playlist.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' '  + str(t) + ' & disown')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      print(cmd)
      by_playlist = by_playlist + 1
      
      sleep(10)  

#run by search process
by_search=1
while(by_search <= int(behaivor_by_search)):
      if(opsy=="Windows"):
         cmd=('start python by_search.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' +  str(t) )
      elif(opsy=="Linux"): 
         cmd=('python3 by_search.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' +  str(t)+ ' & disown')
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
         cmd=('python3 by_save.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' +  str(t) + ' & disown')
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
         cmd=('python3 by_album.py ' + str(behaivor_margin_play) + ' ' + str(id_playlist_album) + ' ' + str(t)  + ' & disown')
      subprocess.call(cmd, shell=True, cwd='scriptes/spotify/')
      print(cmd)
      by_album = by_album + 1
      sleep(10)  