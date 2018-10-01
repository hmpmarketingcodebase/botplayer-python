from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from random import choice 
import random
import sys
import MySQLdb
import datetime
from requests import get
import platform
import heart
sys.path.append("..")
import common.heart
import os
import psutil
try:
   mypubilcip = get('https://api.ipify.org').text
except:
   mypubilcip = "-"
margin_play = sys.argv[1] # margin play(duration of song = 120 seconds # margin play = 20 seconds # then play song between 100 and 120 seconds)
id_playlist = sys.argv[2] # id playlist (list of songs)
part = sys.argv[3] # 
part_sec = 86400 / int(part) # how many seconds in 1 part per day

opsy = platform.system() #operation system (windows or linux)
if (opsy=='Linux'):
   from pyvirtualdisplay import Display
   display = Display(visible=0, size=(1366, 768))
   display.start()
   
pid=10
while(1):
 try:
   if(opsy=='Linux'):
      common.heart.kill_process(pid) 
   driver.close()
 except:
   err=1
 pp=0
 vv=0
 while(vv<int(part)):
  if(opsy=='Linux'):
     common.heart.clean_memory()
  vv=vv+1  
  if(int(part_sec)<1):
      part_sec=2
  tt= int(random.randint(1,int(part_sec)))
  current=datetime.datetime.now()
  ttb = current + datetime.timedelta(0,tt)
  pl1=-1
  print("will be playing at :" + str(ttb) )
  sleep(tt)
  while(pl1<0): 
   try: 
    try:
      id_insert = 0
      state="finish"
      pp=pp+1
#Connection
      cnx = common.heart.connectiondb('deezer')

#get account
      account_=common.heart.account(cnx)
      in_use_account = str(account_[4])
      user_account = str(account_[1]) 
      password_account = str(account_[2])
      id_account = str(account_[0])
#country of account will be the same for proxy and user language
      country = str(account_[3])
      common.heart.account_in_use(in_use_account,id_account,cnx) 
  
#get proxy
      proxy = common.heart.proxis(country,cnx)
      in_use_proxy = str(proxy[3]) 
      #proxy_ip = str(proxy[1])
      proxy_ip = ":"   
      id_proxy = str(proxy[0])       
      usr = str(proxy[5])       
      pwd = str(proxy[6])   
      common.heart.proxy_in_use(in_use_proxy,id_proxy,cnx)

#get random common.heart.songs 
      song = common.heart.songs(id_playlist,cnx)   
  
#get albums
      albums = common.heart.albums_(cnx)
      
#get artist      
      artists = common.heart.artist(cnx)

#log insert (by search type)
      current=datetime.datetime.now()
      next_start = current
      print(user_account + " > Let's Gooo!" )

#common.heart.next_run(next_start,proxy_ip,user_account)
      #common.heart.log_insert(proxy_ip,user_account,str(next_start),"By Search",cnx)
      
#config webdriver
      driver = common.heart.config_driver()
      driver.service.process # is a Popen instance for the chromedriver process
      p = psutil.Process(driver.service.process.pid)
      print("#####################################")
      print ("PID : " + str(p.pid))
      pid = str(p.pid)
      #driver.get("https://whatismyipaddress.com/fr/mon-ip")
      #print("ip is : " + driver.find_element_by_xpath("//div[@id='section_left']//div[2]").text)
#connect to proxy by extension, connexion browser side
      common.heart.proxy_connect(str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]),usr,pwd,driver)
      #view current ip
      #driver.get("http://www.mon-ip.com/info-adresse-ip.php")
      lang = country
      if(country =='us' or country =='gb' or country =='ca' ):
          lang='en'
      common.heart.language_browser(lang,driver) 
#Mobile user agent
      #common.heart.mobile_ua(driver)
      
      driver.get("https://www.deezer.com/login")
      connect_proxy=0

      connect_proxy = heart.check_proxy(driver)
      if(connect_proxy == 0):
         state="Error Proxy!"            
      connect=1
      #check proxy connection
      if(connect_proxy==1):
            #heart.login
            heart.login(driver,user_account,password_account)
            connect=-1
            try:
                 #if it's an invalid account then connect = 0
                 driver.find_element_by_xpath("//div[@id='login_error']")
                 state="Cannot Connect"
                 connect=-1
                 print(user_account +' > ' + state)
            except NoSuchElementException:
                 connect=1
        
            #if connected
            if(connect==1):
                print("connect : account " + user_account)
                url = "https://www.deezer.com/"
                
                try:
                    wait = WebDriverWait(driver, 30)
                    aa = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='dzr-app']//div[@class='page-shadow']//div[@id='notify']//a[@class='message']")))
                    aa.click()
                    print('New Version')
                except:
                    print("--")
                ii=0
                pl=0
                insert=0
                #fetch all songs   
                for s in song:
                    try:      
                        print("----------")   
                        if(opsy=='Linux'):
                           common.heart.clean_memory()
                    #try:      
                        ii=ii+1
                        song_name = s[1]
                        song_duration = int(s[3])
                        song_artist = int(s[6])
                        song_artist_name = ""
                        for a in artists:
                             if(int(a[0]) == song_artist):
                                 song_artist_name = a[1]
                        song_album = int(s[4])
                        song_album_url = ""
                        #get album name of the current song
                        for al in albums:
                             if(int(al[0]) == song_album):
                                 song_album_name = al[1]   
                        print("------****---")

                        heart.top_search(driver,song_name,song_artist_name)
                        xx=0
                        nn=0
                        while((xx<50)and(nn<=0)):
                               try:
                                  song_name_ = str(driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-title']").text).lower()
                                  artist_name_ = str(driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-artist']").text).lower()
                                  album_name_ =  str(driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-album']").text).lower()
                                  song_name = song_name.lower()
                                  song_artist_name = song_artist_name.lower()
                                  song_album_name = song_album_name.lower()
                                  print("song name ^ " + song_name_ + " = " + song_name + " | " )
                                  print("artist name ^ " + artist_name_ + " = " + song_artist_name + " | " )
                                  print("album name ^ " + album_name_ + " = " + song_album_name + " | " )
                                  if ((song_name_.lower() == song_name.lower()) and (song_artist_name.lower() in artist_name_.lower()) and (song_album_name.lower() == album_name_.lower())):
                                       print("--------------------------------------------------------------------------" )
                                       print("song name ^ " + song_name_ + " = " + song_name + " | " )
                                       print("artist name ^ " + artist_name_ + " = " + song_artist_name + " | " )
                                       print("album name ^ " + album_name_ + " = " + song_album_name + " | " )
                                       row =  driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell datagrid-cell-action']")
                                       ActionChains(driver).move_to_element(row).perform()
                                       sleep(1)
                                       row.click()
                                       sleep(5)
                                       if(heart.check_00(driver) == "00:00"):
                                           driver.refresh()
                                           row =  wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell datagrid-cell-action']")))
                                           ActionChains(driver).move_to_element(row).perform()
                                           sleep(1)
                                           row.click()
                                       nn=1
                                       print("--------------------------------------------------------------------------" )
                               except:
                                  err=1
                               xx=xx+1

                        ms=(random.randrange(30, 40))
                        i=0
                        o = ms / 5
                        jj=0
                        kk=0
                        if(nn>0):
                          print("OOOK")
                          while(i<o and jj<1):
                           sleep(5)
                           try:
                                a = driver.find_element_by_xpath("//div[@class='player-bottom']//div[@class='marquee-content']//a[@class='track-link']")
                                zzz = str(a.text).lower()
                                if(int(heart.disonnect(driver) == 1)):
                                    if(opsy=='Linux'):
                                      common.heart.kill_process(pid) 
                                    driver.close()
                                print( ">>> " + zzz)
                                if(zzz == song_name_.lower()):
                                   i=i+1
                                else:
                                   kk=kk+1
                                   if(kk==3):
                                     jj=1
                           except :
                                jj=1
                          row.click()
  
                        if(i >= 6):
                          pl=pl+1
                          if(insert==0):
                                id_insert = common.heart.log_insert(proxy_ip,user_account,str(next_start),mypubilcip,"Search",cnx)
                                print("# id = " + str(id_insert))
                                file = open("log/"+str(id_insert),"w") 
                                nxt=1
                                print("1")
                                insert=1
                          else:
                                print("2")
                                #common.heart.log_update(pl,proxy_ip,user_account,cnx,'deezer')
                                file = open("log/"+str(id_insert),"w") 
                                file.write(str(pl))
                                file.close()
                                if(pl>=3):
                                   pl1=1
                                print("3")
                    except:
                        sleep(1)
                        print("4")
      ##### exceptions 
      try:
          if(opsy=='Linux'):
             common.heart.kill_process(pid) 
          driver.close()
          print("5")
          common.heart.read_log_update(id_insert,cnx,'deezer','../deezer/log/')
      except:
          err=1
          common.heart.read_log_update(id_insert,cnx,'deezer','../deezer/log/')
      
      try:
         cnx = common.heart.connectiondb('deezer')
      except MySQLdb.Error as err:
         print("Error connection")
      if(connect == -1):  
         common.heart.error_account(user_account,password_account,cnx)
      if(connect_proxy != 1):        
         common.heart.error_proxy(in_use_proxy,id_proxy,cnx)
         id_insert = common.heart.log_insert(proxy_ip,user_account,"Error proxy",mypubilcip,"Search",cnx)
      common.heart.finish(proxy_ip,user_account,cnx,state)     
      print(user_account + " > " + state)
    except MySQLdb.Error as err:
       print("----->Error connection")
       common.heart.read_log_update(id_insert,cnx,'deezer','../deezer/log/')
   except :
      try:
          e = sys.exc_info()[0]
          print(str(e))
          if(opsy=='Linux'):
             common.heart.kill_process(pid) 
          driver.close()
          common.heart.read_log_update(id_insert,cnx,'deezer','../deezer/log/')
      except:
          err=1
          common.heart.read_log_update(id_insert,cnx,'deezer','../deezer/log/')
  