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
import heart
from requests import get
from urllib.parse import quote
import platform
import heart
sys.path.append("..")
import common.heart

mypubilcip = get('https://api.ipify.org').text
margin_play = sys.argv[1] # margin play(duration of song = 120 seconds # margin play = 20 seconds # then play song between 100 and 120 seconds)
id_playlist = sys.argv[2] # id playlist (list of songs)
part = sys.argv[3] # 
part_sec = 86400 / int(part) # how many seconds in 1 part per day
opsy = platform.system() #operation system (windows or linux)

if(opsy=='Linux'):
   #for server run with virtual display
   from pyvirtualdisplay import Display
   display = Display(visible=0, size=(1366, 768))
   display.start()
 

while(1):
 pp=0
 vv=0
 while(vv<int(part)):
  vv=vv+1  
  if(int(part_sec)<1):
      part_sec=2
  tt= int(random.randrange(1,int(part_sec)))
  current=datetime.datetime.now()
  ttb = current + datetime.timedelta(0,tt)
  pl1=-1
  play=0
  print("will be playing at :" + str(ttb) )
  sleep(tt)
  while(pl1<0): 
   #try: 
    try:
      state="Finish"
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

#get random heart.songs 
      song = common.heart.songs(id_playlist,cnx)   
  
#get albums
      albums = common.heart.albums_(cnx)
      
#get artist      
      artists = common.heart.artist(cnx)

#log insert (by search type)
      current=datetime.datetime.now()
      next_start = current
      print(user_account + " > Let's Gooo!" )

#next_run(next_start,proxy_ip,user_account)
      #log_insert(proxy_ip,user_account,str(next_start),"By Search",cnx)
      
#config webdriver
      driver = common.heart.config_driver()
#connect to proxy by extension, connexion browser side
      common.heart.proxy_connect(str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]),usr,pwd,driver)
 
      #view current ip
      #driver.get("http://www.mon-ip.com/info-adresse-ip.php")
      lang = country
      #if(country =='us' or country =='uk' ):
      #    lang='en'
      common.heart.language_browser('fr',driver) 
#Mobile user agent
      #heart.mobile_ua(driver)
      common.heart.random_ua(driver,'deezer')
      driver.switch_to.window("t2")
         
      driver.get("https://www.deezer.com/login")
      connect_proxy=0

#check proxy state
      connect_proxy = heart.check_proxy(driver)
      if(connect_proxy == 0):
         state="Error Proxy!"            
      connect=1
      #check proxy connection
      if(connect_proxy==1):
            #login
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
                ii=0
                pl=0
                insert=0
                #fetch all songs   
                for s in song:
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
                        heart.left_search(driver,song_name,song_artist_name)
                        xx=0
                        nn=0
                        while((xx<50)and(nn<=0)):
                               try:
                                  song_name_ = driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-title']").text
                                  artist_name_ = driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-artist']").text
                                  album_name_ =  driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-album']").text
                                  print("song name ^ " + song_name_ + " = " + song_name + " | " )
                                  print("artist name ^ " + artist_name_ + " = " + song_artist_name + " | " )
                                  print("album name ^ " + album_name_ + " = " + song_album_name + " | " )
                                  if ((song_name_ == song_name) and (song_artist_name in artist_name_) and (song_album_name == album_name_)):
                                       print("+ " + song_name_ + "+ " + artist_name_ + " + " + album_name_)
                                       row =  driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']")
                                       ActionChains(driver).double_click(row).perform()
                                       nn=1
                               except:
                                  err=1
                               xx=xx+1
  
                        if(pp%10==0):
                                 ms=(random.randrange(int(song_duration) - int(margin_play) , int(song_duration)))
                        else:
                                 ms=(random.randrange(40, 80))
                        print(" > Playing : " + song_name + " in " + str(ms) + " seconds")
                        i=0
                        o = ms / 5
                        while(i<o):
                           sleep(5)
                           try:
                                driver.find_element_by_xpath("//div[@id='modal_limitation']//button[@class='btn btn-primary']").click()
                                print("disconnect all other devices")
                           except :
                                try:
                                    driver.find_element_by_xpath("//div[@id='page_sidebar']//button[@class='control control-play']//span[@class='icon icon-play']")
                                    driver.find_element_by_xpath("//div[@id='page_sidebar']//button[@class='control control-play']").click()
                                    i=i+1
                                    print("palying >")
                                except:
                                    print("playing >>")
                                    i=i+1
                        print("yeaaah!!")
                        play=play+1
                        if(play == 3):
                             pl1=1
                        sleep(2)
                        if(insert==0):
                             common.heart.log_insert(proxy_ip,user_account,str(next_start),mypubilcip,"Search",cnx)
                             insert=1
                        else:
                             common.heart.log_update(ii,proxy_ip,user_account,cnx,'deezer')                      
                    #except:
                  #      sleep(1)
                  
      ##### exceptions 
      try:
         driver.close() 
      except :
         sleep(1)
      
      try:
         cnx = common.heart.connectiondb('deezer')
      except MySQLdb.Error as err:
         print("Error connection")
      if(connect == -1):  
         common.heart.error_account(user_account,password_account,cnx)
      if(connect_proxy != 1):        
         common.heart.error_proxy(in_use_proxy,id_proxy,cnx)
      print(state)
      common.heart.finish(proxy_ip,user_account,cnx,state)     
      print(user_account + " > " + state)
    except MySQLdb.Error as err:
       print("----->Error connection")
       common.heart.finish(proxy_ip,user_account,cnx,"max request limit")
  # except :   
  #    print("error")
  #    try:
  #       driver.close() 
  #    except:  
  #       sleep(1)