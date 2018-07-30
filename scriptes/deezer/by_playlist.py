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
sys.path.append("..")
import common.heart
from requests import get
from urllib.parse import quote
import platform

mypubilcip = get('https://api.ipify.org').text
margin_play = sys.argv[1] # margin play(duration of song = 120 seconds # margin play = 20 seconds # then play song between 100 and 120 seconds)
id_playlist = sys.argv[2] # id playlist (list of songs)
playlist_name = sys.argv[3] #operation system (windows or linux)
part = sys.argv[4] # 
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
      common.heart.proxy_in_use(in_use_proxy,id_proxy,cnx)

#get random songs 
      song = common.heart.songs(id_playlist,cnx)   
      song_ = song   
  
#get albums
      albums = common.heart.albums_(cnx)
      
#get artist      
      artists = common.heart.artist(cnx)

#log insert (by search type)
      current=datetime.datetime.now()
      next_start = current
      print(user_account + " > Let's Gooo!" )

#next_run(next_start,proxy_ip,user_account)
      #common.heart.log_insert(proxy_ip,user_account,str(next_start),"By Search",cnx)
      
#config webdriver
      driver = common.heart.config_driver()
      #driver.get("https://whatismyipaddress.com/fr/mon-ip")
      #print("ip is : " + driver.find_element_by_xpath("//div[@id='section_left']//div[2]").text)
#connect to proxy by extension, connexion browser side
      common.heart.proxy_connect(str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]),driver)
 
      #view current ip
      #driver.get("http://www.mon-ip.com/info-adresse-ip.php")
      lang = country
      #if(country =='us' or country =='uk' ):
      #    lang='en'
      common.heart.language_browser('fr',driver) 
#Mobile user agent
      #common.heart.mobile_ua(driver)
      common.heart.random_ua(driver,'deezer')
      driver.switch_to.window("t2")
         
      driver.get("https://www.deezer.com/login")
      connect_proxy=0
#check proxy state
      connect_proxy = heart.check_proxy(driver)
      if(connect_proxy == 0):
         state="Error Proxy!"

      continue_=0      
      connect=1
      #check proxy connection
      if(connect_proxy==1):
            #login
            wait = WebDriverWait(driver, 30)
            heart.login(driver,user_account,password_account)
            connect=-1
            try:
                 #if it's an invalid deezer account then connect = 0
                 driver.find_element_by_xpath("//div[@id='login_error']")
                 state="Cannot Connect"
                 connect=-1
                 print(user_account +' > ' + state)
            except NoSuchElementException:
                 connect=1
            continue_=0           #if connected
            if(connect==1):
                print("connect : account " + user_account)
                #come back to default ua
                url = "https://www.deezer.com/"
                driver.get(url)
                wait.until(EC.element_to_be_clickable((By.ID, "menu_search")))
                continue_= heart.search_playlist(driver,playlist_name)
                sleep(5)
                print('# continue = ' + str(continue_) )
                if(continue_==1):
                    #get search input element
                    pl=0
                    insert=0
                    #fetch all songs   
                    for s in song:
                    #try:      
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
                        sleep(5)
                        xx=0
                        nn=0
                        #Add to playlist
                        while((xx<50)and(nn<=0)):
                               try:
                                  song_name_ = driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-title']").text
                                  artist_name_ = driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-artist']").text
                                  album_name_ =  driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-album']").text
                                  print("song name ^ " + song_name_ + " = " + song_name + " | " )
                                  if ((song_name_ == song_name) and (song_artist_name in artist_name_) and (song_album_name == album_name_)):
                                       print("+ " + song_name_ + "+ " + artist_name_ + " + " + album_name_)
                                       try:
                                          l =  wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']")))
                                          ActionChains(driver).move_to_element(l).perform() 
                                          wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell datagrid-cell-hover datagrid-cell-action']//button[@class='action-item-btn datagrid-action']"))).click()
                                          wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='label ellipsis' and contains(text(), '"+playlist_name+"')]"))).click()
                                          print( song_name_ + " To " + album_name_)
                                          sleep(5) 
                                       except:
                                          err=1
                                       
                                       nn=1
                               except:
                                  err=1
                               xx=xx+1
                    heart.search_playlist(driver,playlist_name)
                    pl1 = heart.right_search_and_play(driver,song_,artists,albums,"playlist",pp,proxy_ip,user_account,next_start,mypubilcip,cnx)
                else:
                    try:
                       wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='create-assistant-container']"))).click()
                       aa = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='assistant-info']//input[@class='form-control form-control-block']")))
                       aa.click()
                       aa.send_keys(playlist_name)
                       wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='modal_playlist_assistant_submit']"))).click()
                       sleep(5)
                    except:
                       driver.refresh()
                       wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='create-assistant-container']"))).click()
                       aa = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='assistant-info']//input[@class='form-control form-control-block']")))
                       aa.click()
                       aa.send_keys(playlist_name)
                       wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='modal_playlist_assistant_submit']"))).click()
                       sleep(5)
                    #get search input element
                    pl=0
                    insert=0
                    #fetch all songs   
                    for s in song:
                    #try:      
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
                        sleep(5)
                        xx=0
                        nn=0
                        #Add to playlist
                        while((xx<50)and(nn<=0)):
                               try:
                                  song_name_ = driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-title']").text
                                  artist_name_ = driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-artist']").text
                                  album_name_ =  driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-album']").text
                                  print("song name ^ " + song_name_ + " = " + song_name + " | " )
                                  if ((song_name_ == song_name) and (song_artist_name in artist_name_) and (song_album_name == album_name_)):
                                       print("+ " + song_name_ + "+ " + artist_name_ + " + " + album_name_)
                                       try:
                                          l =  wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']")))
                                          ActionChains(driver).move_to_element(l).perform() 
                                          wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell datagrid-cell-hover datagrid-cell-action']//button[@class='action-item-btn datagrid-action']"))).click()
                                          wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='label ellipsis' and contains(text(), '"+playlist_name+"')]"))).click()
                                          print( song_name_ + " To " + album_name_)
                                          sleep(5) 
                                       except:
                                          err=1
                                       
                                       nn=1
                               except:
                                  err=1
                               xx=xx+1
                    heart.search_playlist(driver,playlist_name)
                    pl1 = heart.right_search_and_play(driver,song_,artists,albums,"playlist",pp,proxy_ip,user_account,next_start,mypubilcip,cnx)
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