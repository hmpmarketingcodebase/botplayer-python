import math
from time import sleep
import sys
import MySQLdb
import datetime
import subprocess
sys.path.insert(0, 'python_files/')
from heart import connectiondb

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
#country id (from country table)
country=sys.argv[4] 
#id playlist album
id_playlist_album=sys.argv[5]    
#id playlist
id_playlist=sys.argv[6]
#os (windows or linux)
opsy=sys.argv[7]

os.system("git pull origin master & disown")
sleep(20)
os.system("chmod -R 777 shell")
os.system("chmod -R 777 tools")
sleep(10)
print("Ready!!")
#Connection
try:
  cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.","spoti")
  cursor = cnx.cursor()
except MySQLdb.Error as err:
  print("Error connection")

#insert robot datas 
try:
    cmd="INSERT INTO `robot`(`name`, `start_date`, `behaivor`,`id_playlist`,`id_playlist_album`, `number_threads`, `running`, `country`) VALUES ('"+str(name) + "', '"+str(start_date)+"', "+str(behaivor)+", "+str(id_playlist)+", "+str(id_playlist_album)+", "+str(number_threads)+", "+str(running)+", '" + str(country) + "')"
    cursor.execute(cmd)
    cnx.commit() 
except MySQLdb.Error as err:
    print("Something went wrong: {}".format(err))

i=0

#get playlist
try:
   cursor.execute("select * from playlist where id = " + id_playlist)  
   playlists = cursor.fetchone()
   url_playlist = str(playlists[2]) 
   name_playlist = str(playlists[1]) 
except MySQLdb.Error as err:  
   print("Something went wrong: (Accounts) {}".format(err))   

#get playlist_album
try:
   cursor.execute("select * from playlist_album where play = " + id_playlist_album)  
   playlist_album = cursor.fetchone()
   id_album = str(playlist_album[1])  
except MySQLdb.Error as err:  
   print("Something went wrong: (Accounts) {}".format(err))
   
#get album
try:
   cursor.execute("select * from album where id = " + id_album)  
   albums = cursor.fetchone()
   url_album = str(albums[2]) 
   name_album = str(albums[1]) 
except MySQLdb.Error as err:  
   print("Something went wrong: (Accounts) {}".format(err))   
 

#get behaivor
try:
   cursor.execute("select * from behaivor where id = " + behaivor)  
   behaivor = cursor.fetchone() 
   behaivor_by_playlist=behaivor[2] # % 
   behaivor_by_album=behaivor[4] # %
   behaivor_by_search=behaivor[5] # %
   behaivor_by_direct_save=behaivor[6] # % 
   behaivor_margin_play=behaivor[7] 
   
except MySQLdb.Error as err:  
   print("Something went wrong: (Behaivor) {}".format(err))   

#manage and call thread (percentage)
behaivor_by_playlist = math.floor(int(behaivor_by_playlist) * int(number_threads) / 100)
behaivor_by_album = math.floor(int(behaivor_by_album) * int(number_threads) / 100)
behaivor_by_search = math.floor(int(behaivor_by_search) * int(number_threads) / 100)
behaivor_by_save = math.floor(int(behaivor_by_direct_save) * int(number_threads) / 100)

#run by playlist process
by_playlist=1
while(by_playlist <= int(behaivor_by_playlist)):
      if(opsy=="windows"):         
         cmd=('start by_playlist.bat ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' + str(country) +  ' ' + str(name_playlist) + ' ' + opsy )
         subprocess.call(cmd, shell=True, cwd='shell/windows/')
      elif(opsy=="linux"):
         cmd=('./by_playlist.sh ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' + str(country) +  ' ' + str(name_playlist) + ' ' + opsy + ' & disown')
         subprocess.call(cmd, shell=True, cwd='shell/linux/')
      print(cmd)
      by_playlist = by_playlist + 1
      
      sleep(10)  

#run by search process
by_search=1
while(by_search <= int(behaivor_by_search)):
      if(opsy=="windows"):
         cmd=('start by_search.bat ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' + str(country) + ' ' + opsy )
         subprocess.call(cmd, shell=True, cwd='shell/windows/')
      elif(opsy=="linux"): 
         cmd=('./by_search.sh ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' + str(country) + ' ' + opsy + ' & disown')
         subprocess.call(cmd, shell=True, cwd='shell/linux/')
      print(cmd)
      by_search = by_search + 1
      sleep(10)  

#run by direct save process
by_save=1
while(by_save <= int(behaivor_by_save)):
      if(opsy=="windows"):
         cmd=('start by_save.bat ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' + str(country) + ' ' + opsy )
         subprocess.call(cmd, shell=True, cwd='shell/windows/')
      elif(opsy=="linux"):
         cmd=('./by_save.sh ' + str(behaivor_margin_play) + ' ' + str(id_playlist) + ' ' + str(country) + ' ' + opsy + ' & disown')
         subprocess.call(cmd, shell=True, cwd='shell/linux/')
      print(cmd)
      by_save = by_save + 1
      sleep(10)  

#run by album process
by_album=1
while(by_album <= int(behaivor_by_album)):
      if(opsy=="windows"):
         cmd=('start by_album.bat ' + str(behaivor_margin_play) + ' ' + str(id_playlist_album) + ' ' + str(country) + ' ' + opsy )
         subprocess.call(cmd, shell=True, cwd='shell/windows/')
      elif(opsy=="linux"):
         cmd=('./by_album.sh ' + str(behaivor_margin_play) + ' ' + str(id_playlist_album) + ' ' + str(country) + ' ' + opsy + ' & disown')
         subprocess.call(cmd, shell=True, cwd='shell/linux/')
      print(cmd)
      by_album = by_album + 1
      sleep(10)  
