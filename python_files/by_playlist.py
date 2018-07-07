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
name_playlist = sys.argv[4] # name of playlist 
opsy = sys.argv[5] #operation system (windows or linux)

if(opsy=='linux'):
   #for server run with virtual display
   from pyvirtualdisplay import Display
   display = Display(visible=0, size=(1366, 768))
   display.start()
   
pp=0
while(1):
 try: 
  try:
      state="Finish"
      pp=pp+1
#Connection
      cnx = connectiondb()

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
      song_s = song
#get albums
      albums = albums_(cnx)
      
#get artist      
      artists = artist(cnx)

#log insert (by playlist type)
      current=datetime.datetime.now()
      next_start = current
      print(user_account + " > Start at :" + str(next_start) )
      log_insert(proxy_ip,user_account,str(next_start),"By Playlist",cnx)
      # next_run(next_start,proxy_ip,user_account)

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
      wait = WebDriverWait(driver, 30)

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
              print (user_account + " > Loading took too much time! (proxy)")
              connect_proxy=0
              state="Error Proxy!" 
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

                url = "https://open.spotify.com/collection/playlists"
                driver.get(url)
                try:
                   a = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "//div[@class='terms-of-service-modal__buttons-container']//button[@class='btn btn-green']"))) 
                   a.click()
                   print("agree")
                   sleep(5) 
                except:
                   sleep(5) 
                   
                # if name of playlist already exist delete and create another
                try:
                    driver.execute_script("window.scrollBy(0, 1000);")
                    sleep(1)
                    w = WebDriverWait(driver, 5)
                    a = w.until(EC.visibility_of_element_located((By.XPATH, "//section[@class='contentSpacing']//div[@class='container-fluid container-fluid--noSpaceAround']//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-2']//a[@title='"+name_playlist+"']")))
                    playlist_ = w.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='contentSpacing']//div[@class='container-fluid container-fluid--noSpaceAround']//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-2']")))
                    ActionChains(driver).context_click(playlist_).perform() 
                    delete = w.until(EC.visibility_of_element_located((By.XPATH, "//nav[@class='react-contextmenu react-contextmenu--visible']//div[3][@class='react-contextmenu-item']")))
                    ActionChains(driver).move_to_element(delete).perform() 
                    cl = w.until(EC.element_to_be_clickable((By.XPATH, "//nav[@class='react-contextmenu react-contextmenu--visible']//div[3][@class='react-contextmenu-item react-contextmenu-item--selected']")))
                    cl.click()
                    a = w.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button-group button-group--horizontal']//div[@class='button-group__item']//button[@class='btn btn-green']")))
                    a.click()
                    sleep(5)
                except TimeoutException:
                  try:
                    driver.get(url)
                    driver.execute_script("window.scrollBy(0, 1000);")
                    sleep(1)
                    w = WebDriverWait(driver, 5)
                    a = w.until(EC.visibility_of_element_located((By.XPATH, "//section[@class='contentSpacing']//div[@class='container-fluid container-fluid--noSpaceAround']//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-2']//a[@title='"+name_playlist+"']")))
                    playlist_ = w.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='contentSpacing']//div[@class='container-fluid container-fluid--noSpaceAround']//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-2']")))
                    ActionChains(driver).context_click(playlist_).perform() 
                    delete = w.until(EC.visibility_of_element_located((By.XPATH, "//nav[@class='react-contextmenu react-contextmenu--visible']//div[3][@class='react-contextmenu-item']")))
                    ActionChains(driver).move_to_element(delete).perform() 
                    cl = w.until(EC.element_to_be_clickable((By.XPATH, "//nav[@class='react-contextmenu react-contextmenu--visible']//div[3][@class='react-contextmenu-item react-contextmenu-item--selected']")))
                    cl.click()
                    a = w.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button-group button-group--horizontal']//div[@class='button-group__item']//button[@class='btn btn-green']")))
                    a.click()
                    sleep(5)
                  except TimeoutException:
                    sleep(1)
                # create playlist
                try:
                    driver.get(url)
                    playlist_ = w.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='asideButton']//button[@class='btn btn-green btn-small asideButton-button']")))
                    playlist_.click()
                    sleep(5)
                    print(user_account + " > Crate Playlist : " + name_playlist)
                except WebDriverException:
                    driver.get(url)
                    playlist_ = w.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='asideButton']//button[@class='btn btn-green btn-small asideButton-button']")))
                    playlist_.click()
                    sleep(5)
                    print(user_account + " > Crate Playlist : " + name_playlist)

                try: 
                    input = w.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='inputBox']//input[@class='inputBox-input']")))
                    input.clear()
                    sleep(5)
                    input.clear()
                    sleep(5)

                    input.send_keys(name_playlist)
                    a = w.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button-group button-group--horizontal']//button[@class='btn btn-green']")))
                    a.click()
                    sleep(5)  
                except TimeoutException:
                    sleep(1)
                driver.get("https://open.spotify.com/browse/featured")

                try:
                  try:
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
                #get search input element                
                search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.inputBox-input")))
                #fetch all songs  
                for s in song:                
                        song_name = s[1]
                        song_duration = int(s[3])
                        song_artist = int(s[6])
                        song_artist_name = ""
                        # get artist of current song
                        for a in artists:
                             if(int(a[0]) == song_artist):
                                 song_artist_name = a[1] 
                        song_album = int(s[4])
                        song_album_url = ""
                        # get album of current song
                        for al in albums:
                             if(int(al[0]) == song_album):
                                 song_album_url = al[2] 
                                 song_album_url = song_album_url[24:]   
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
                              driver.refresh()
                              search.clear()
                              sleep(5)
                              search.clear()
                              sleep(5)
                              search.send_keys(song_name + " " + song_artist_name)
                              try:
                                wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[contains(text(), '"+song_name+"')]")))
                              except TimeoutException:
                                sleep(2)   
                        
                        x=0
                        nn=0
                        while((x<=50)and(nn<=0)):
                          try:
                            x=x+1
                            # get song result
                            txt = driver.find_element_by_xpath("//section[@class='tracklist-container']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[@class='second-line ellipsis-one-line']//a[@href='"+song_album_url+"']")
                            men = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")
                            # move cursor to song                             
                            ActionChains(driver).move_to_element(men).perform()                    
                            sleep(2)
                            # right click
                            men2 = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")               
                            ActionChains(driver).context_click(men2).perform() 
                            sleep(2)
                            # click add 
                            save = driver.find_element_by_xpath("//nav[@class='react-contextmenu react-contextmenu--visible']//div[4][@class='react-contextmenu-item']")
                            print(save.text)
                            if (("Add" in save.text) or ("Ajouter" in save.text)):
                                nn=1
                                ActionChains(driver).move_to_element(save).perform() 
                                sleep(1)
                                save.click()
                                sleep(3)
                                print(user_account + " > " + song_name + " to Playlist : " )
                            try:         
                                pplay = driver.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar__left']//div[@class='track-info ellipsis-one-line']//div[@class='track-info__name ellipsis-one-line']//div[@class='react-contextmenu-wrapper']").text 
                            except:
                                driver.refresh()
                                sleep(5)
                                try:
                                    pplay = driver.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar__left']//div[@class='track-info ellipsis-one-line']//div[@class='track-info__name ellipsis-one-line']//div[@class='react-contextmenu-wrapper']").text 
                                except:
                                    driver.close()
 
                          except NoSuchElementException:
                            print("1")

                        nn=0
                        x=0
                        # find playlist and add song
                        while((x<=50)and(nn<=0)):
                          try:
                            x=x+1
                            biblio = driver.find_element_by_xpath("//div[@class='dialog dialog--without-background']//div[@class='container-fluid container-fluid--noSpaceAround']//div['"+str(x)+"'][@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-2']//div[@class='mo-info']")         
                            if(biblio.text == name_playlist):
                                add = driver.find_element_by_xpath("//div[@class='dialog dialog--without-background']//div[@class='container-fluid container-fluid--noSpaceAround']//div['"+str(x)+"'][@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-2']")
                                ActionChains(driver).move_to_element(add).perform()                    
                                sleep(2)                    
                                add.click()                    
                                sleep(5)                    
                                nn=1
                          except NoSuchElementException:
                            print("+")
                sleep(2)     
                # click library > left menu
                try:
                   biblio = driver.find_element_by_xpath("//div[@class='navBar-expand']//li[3][@class='navBar-group']")         
                   biblio.click()                   
                except:
                   try:
                       driver.refresh()
                       biblio = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='navBar-expand']//li[3][@class='navBar-group']")))
                       biblio.click()                   
                   except:
                       try:
                          driver.refresh()
                          biblio = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='navBar-expand']//li[3][@class='navBar-group']")))
                          biblio.click()                   
                       except:
                          driver.refresh()
                          biblio = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='navBar-expand']//li[3][@class='navBar-group']")))
                          biblio.click()  
                    
                #driver.get("https://open.spotify.com/collection/playlists")
                
                try:
                  try:
                      # click playlist tab 
                      a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/collection/playlists']")))
                      a.click()
                      driver.execute_script("window.scrollBy(0, 1000);")
                      a = wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='contentSpacing']//div[@class='container-fluid container-fluid--noSpaceAround']//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-2']//a[@title='"+name_playlist+"']")))
                      a.click()                 
                      print(user_account + " > List of playlist")
                  except NoSuchElementException:
                      driver.get("https://open.spotify.com/collection/playlists")
                      a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/collection/playlists']")))
                      a.click()
                      driver.execute_script("window.scrollBy(0, 1000);")
                      a = wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='contentSpacing']//div[@class='container-fluid container-fluid--noSpaceAround']//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-2']//a[@title='"+name_playlist+"']")))
                      a.click()                 
                      print(user_account + " > List of playlist")
                except NoSuchElementException:
                  driver.get("https://open.spotify.com/collection/playlists")
                  a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/collection/playlists']")))
                  a.click()
                  driver.execute_script("window.scrollBy(0, 1000);")
                  a = wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='contentSpacing']//div[@class='container-fluid container-fluid--noSpaceAround']//div[@class='col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-2']//a[@title='"+name_playlist+"']")))
                  a.click()                 
                  print(user_account + " > List of playlist")
                
                ii=0                
                # wait result list
                wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']")))
                for s in song_s:
                        ii=ii+1                
                        song_name = s[1]
                        song_artist = int(s[6])
                        song_artist_name = ""
                        for a in artists:
                             if(int(a[0]) == song_artist):
                                 song_artist_name = a[1] 
                        sleep(2)
                        #change curent device to webdriver device 
                        change_device(driver)
                        sleep(2)
                        change_device(driver)
             
                        song_album = int(s[4])
                        song_album_url = ""
                        for al in albums:
                             if(int(al[0]) == song_album):
                                 song_album_url = al[2] 
                                 song_album_url = song_album_url[24:]   
                                 song_album_name = al[1]   
                        x=0 
                        nn=0
                        driver.execute_script("window.scrollBy(0, 1000);")
                        while((x<=50)and(nn<=0)):
                          try:
                             x=x+1
                             txt = driver.find_element_by_xpath("//section[@class='tracklist-container']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[@class='tracklist-name']")
                             txt2 = driver.find_element_by_xpath("//section[@class='tracklist-container']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[@class='second-line ellipsis-one-line']//span[3]")
                             if(song_name == txt.text and txt2.text==song_album_name):
                               print("x = " + str(x) + " <" + song_name +"|"+ txt.text +">" + "<"  + txt2.text + "|" + song_album_name + ">")
                               # find song and doubleclick
                               doubleclick(driver,x,song_album_url)
                               sleep(5)
                               if(replay(driver)==1):
                                  doubleclick(driver,x,song_album_url)
                               if(pp%10==0):                                                
                                  ms=(random.randrange(int(song_duration) - int(margin_play) , int(song_duration)))
                               else:
                                  ms=(random.randrange(40, 80))
                               print(user_account + " > Playing : " + song_name + " in " + str(ms) + " seconds")
                               player_(driver,song_name,ms,x,song_album_url,proxy_ip,user_account,cnx,ii)
                               nn=1
                          except NoSuchElementException:
                            sleep(1)                                  
   ###exceptions             
      try:
         driver.close() 
      except:
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
  except MySQLdb.Error as err:
       print("----->Error connection")
       sleep(600)
 except :
      print("error")
      try:
         driver.close() 
      except:
         
         sleep(1)
