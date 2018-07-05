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
from proxy_function import proxy_connect
from heart import connectiondb
from heart import replay
from heart import doubleclick
from heart import player_
from heart import change_device
from heart import proxis
from heart import proxy_in_use
from heart import account
from heart import account_in_use
from heart import songs
from heart import albums_
from heart import artist
from heart import log_insert
from heart import config_driver
from heart import next_run
from heart import mobile_ua
from heart import login
from heart import default_ua
from heart import finish
from heart import error_account
from heart import error_proxy


margin_play = sys.argv[1] # margin play(duration of song = 120 seconds # margin play = 20 seconds # then play song between 100 and 120 seconds)
id_playlist = sys.argv[2] # id playlist (list of songs)
country = sys.argv[3] # country of proxy if filter needed 1 = all countries
opsy = sys.argv[4] #operation system (windows or linux)

if(opsy=='linux'):
   #for server run with virtual display
   from pyvirtualdisplay import Display
   display = Display(visible=0, size=(1366, 768))
   display.start()

pp=0
while(1):
 
      state="Finish"
      pp=pp+1
#Connection
      try:
        cnx = connectiondb()
      except MySQLdb.Error as err:
        print("Error connection")

#get proxy
      proxy = proxis(country,cnx)
      in_use_proxy = str(proxy[3]) 
      proxy_ip = str(proxy[1])
      #proxy_ip = ":"  
      id_proxy = str(proxy[0])       
      proxy_in_use(in_use_proxy,id_proxy,cnx)

#get account
      account_=account(country,cnx)
      in_use_account = str(account_[4])
      user_account = str(account_[1]) 
      password_account = str(account_[2])
      id_account = str(account_[0])      
      account_in_use(in_use_account,id_account,cnx)

#get random songs 
      song = songs(id_playlist,cnx)   
  
#get albums
      albums = albums_(cnx)
      
#get artist      
      artists = artist(cnx)

#log insert (by search type)
      current=datetime.datetime.now()
      next_start = current
      print(user_account + " > Start at :" + str(next_start) )

#next_run(next_start,proxy_ip,user_account)
      log_insert(proxy_ip,user_account,str(next_start),"By Search",cnx)
      
#config webdriver
      driver = config_driver(opsy)
      
#connect to proxy by extension, connexion browser side
      proxy_connect(str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]),driver)
 
      #view current ip
      #driver.get("http://www.mon-ip.com/info-adresse-ip.php")

#Mobile user agent
      mobile_ua(driver)
      
      driver.get("https://accounts.spotify.com/en/login")
      connect_proxy=0

#if authentication successfully then connect_proxy = 1 and continue ## if not reload by other proxy
      try:
          WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login-username')))
          print (user_account + " > Proxy is ready!")
          connect_proxy=1
      except TimeoutException:
          try:
              driver.get("https://accounts.spotify.com/en/login")
              WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login-username')))
              print (user_account + " > Proxy is ready!")
              connect_proxy=1
          except TimeoutException:
              driver.get("https://accounts.spotify.com/en/login")
              print (user_account + " > Loading took too much time! (proxy)")
              connect_proxy=0
              state="Error Proxy!" 
              try:
                 driver.close() 
              except WebDriverException:
                 sleep(1)
          
      connect=1
      #check proxy connection
      if(connect_proxy==1):
            #login
            login(driver,user_account,password_account)
            connect=-1
            try:
                 #if it's an invalid spotify account then connect = 0
                 driver.find_element_by_xpath("//p[@class='alert alert-warning']")                   
                 connect=0
                 print (user_account + " > Cannot connect")
                 state="Error Account!"
            except NoSuchElementException:
                 connect=1
        
            #if connected
            if(connect==1):
                print("connect : account " + user_account)
                #come back to default ua
                default_ua(driver)
                driver.get("https://open.spotify.com/browse/featured")
                
                try:
                  try:
                      wait = WebDriverWait(driver, 30)
                      # click search if not fin reload page X 2 if not exist quit and reload other
                      a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-subtle.navBar-link.ellipsis-one-line")))
                      a.click()
                  except TimeoutException:
                      driver.get("https://open.spotify.com/browse/featured")
                      a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-subtle.navBar-link.ellipsis-one-line")))
                      a.click()
                except TimeoutException:
                  driver.get("https://open.spotify.com/browse/featured")
                  a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-subtle.navBar-link.ellipsis-one-line")))
                  a.click()
                try:   
                 try: 
                   #get search input element
                   search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.inputBox-input")))
                   ii=0
                   #fetch all songs 
                   for s in song:          
                        ii=ii+1
                        song_name = s[1]
                        song_duration = int(s[3])
                        song_artist = int(s[6])
                        song_artist_name = ""
                        for a in artists:
                             if(int(a[0]) == song_artist):
                                 song_artist_name = a[1]
                        #put song + artist search input
                        search.clear()
                        sleep(5)
                        search.clear()
                        sleep(5)
                        search.send_keys(song_name + " " + song_artist_name)
                        try:
                           #wait until the result appears if not clean search input and put again other search X2 ## if not exit reload other
                           wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[contains(text(), '"+song_name+"')]")))
                        except TimeoutException:
                           search.clear()
                           sleep(5)
                           search.clear()
                           sleep(5)
                           search.send_keys(song_name + " " + song_artist_name)
                           try:
                              wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[contains(text(), '"+song_name+"')]")))
                           except TimeoutException:
                              search.clear()
                              sleep(2)
                              search.clear()
                              sleep(2)
                              search.send_keys(song_name + " " + song_artist_name)
                              try:
                                wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[contains(text(), '"+song_name+"')]")))
                              except TimeoutException:
                                sleep(2)   
                         
                        song_album = int(s[4])
                        song_album_url = ""
                        #get album name of the current song
                        for al in albums:
                             if(int(al[0]) == song_album):
                                 song_album_url = al[2] 
                                 song_album_url = song_album_url[24:]   
                                 song_album_name = al[1]   
                        x=0
                        nn=0
                        #change curent device to webdriver device 
                        change_device(driver)
                        sleep(1)
                        change_device(driver)

                        while((x<=50)and(nn<=0)):
                          x=x+1
                          # double click to play
                          doubleclick(driver,x,song_album_url)
                          sleep(5)
                          try:
                             txt = driver.find_element_by_xpath("//section[@class='tracklist-container']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[@class='tracklist-name']")
                             txt2 = driver.find_element_by_xpath("//section[@class='tracklist-container']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[@class='second-line ellipsis-one-line']//span[3]")
                            
                             if(song_name == txt.text and txt2.text==song_album_name):
                                # if song state = pause or play = other song > replay
                                if(replay(driver)==1):
                                   doubleclick(driver,x,song_album_url)
                                  
                                # play 9 song between 60 and 80 seconds and 1 between song_duration variable and margin_play variable (song_duration and margin_play in database behivor table)
                                if(pp%10==0):                                                
                                    ms=(random.randrange(int(song_duration) - int(margin_play) , int(song_duration)))
                                else:
                                    ms=(random.randrange(40, 80))
                                print(user_account + " > Playing : " + song_name + " in " + str(ms) + " seconds")
                                player_(driver,song_name,ms,x,song_album_url,proxy_ip,user_account,cnx,ii)
                                nn=1
                          except NoSuchElementException:
                             print("x+")

                 except StaleElementReferenceException:
                     sleep(1)    
                except NoSuchElementException:     
                   sleep(1)   
      ##### exceptions 
      try:
         driver.close() 
      except WebDriverException:
         sleep(1)
      
      try:
         driver.close() 
      except WebDriverException:
         sleep(1)
      try:
         cnx = connectiondb()
      except MySQLdb.Error as err:
         print("Error connection")
      if(connect != 1):  
         error_account(user_account,password_account,cnx)
      if(connect_proxy != 1):        
         error_proxy(in_use_proxy,id_proxy,cnx)
      finish(proxy_ip,user_account,cnx,state)     
      print(user_account + " > " + state)

