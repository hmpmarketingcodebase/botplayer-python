from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
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
import heart
import platform
sys.path.append("..")
import common.heart
import psutil

#get public ip
try:
   mypubilcip = get('https://api.ipify.org').text
except:
   mypubilcip = "-"


margin_play = sys.argv[1] # margin play(duration of song = 120 seconds # margin play = 20 seconds # then play song between 100 and 120 seconds)
id_playlist = sys.argv[2] # id playlist (list of songs)
part = sys.argv[3] # 
part_sec = 86400 / int(part) # how many seconds in 1 part per day
opsy = platform.system()

if(opsy=='Linux'):
   #for server run with virtual display
   from pyvirtualdisplay import Display
   display = Display(visible=0, size=(1366, 768))
   display.start()

pid=10
while(1):
 
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
      state="Finish"
      pp=pp+1
#Connection
      cnx = common.heart.connectiondb('spoti')

#get account
      account_=common.heart.account(cnx)
      in_use_account = str(account_[4])
      user_account = str(account_[1]) 
      password_account = str(account_[2])
      id_account = str(account_[0])
#lang of account will be the same for proxy and user language
      country = str(account_[3])
      common.heart.account_in_use(in_use_account,id_account,cnx) 
  
#get proxy
      proxy = common.heart.proxis(country,cnx)
      in_use_proxy = str(proxy[3]) 
      proxy_ip = str(proxy[1])
      #proxy_ip = ":"  
      id_proxy = str(proxy[0])       
      usr = str(proxy[5])       
      pwd = str(proxy[6])   
      common.heart.proxy_in_use(in_use_proxy,id_proxy,cnx)

#get random songs 
      song = common.heart.songs(id_playlist,cnx)   
      song_s = song

#get albums
      albums = common.heart.albums_(cnx)
      
#get artist      
      artists = common.heart.artist(cnx)
#log insert (by save type)
      current=datetime.datetime.now()
      next_start = current
      print(user_account + " > Let's Goo!" )
      
#config webdriver
      driver = common.heart.config_driver()
      driver.service.process # is a Popen instance for the chromedriver process
      p = psutil.Process(driver.service.process.pid)
      print("#####################################")
      print ("PID : " + str(p.pid))
      pid = str(p.pid)
      
#connect to proxy by extension, connexion browser side
      common.heart.proxy_connect(str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]),usr,pwd,driver)
     
      #view current ip
      #driver.get("http://www.mon-ip.com/info-adresse-ip.php")
      lang = country
      if(country =='us' or country =='uk' ):
          lang='en'
      common.heart.language_browser(lang,driver)
#Mobile user agent
      common.heart.mobile_ua(driver)

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
              print (user_account + " > Loading took too much time! (proxy)")
              connect_proxy=0
              state="Error Proxy!" 
              
      connect=1
      #check proxy connection
      if(connect_proxy==1):
            #login
            common.heart.login(driver,user_account,password_account)
            try:
                 #if it's an invalid spotify account then connect = 0
                 driver.find_element_by_xpath("//p[@class='alert alert-warning']")
                 connect=0
                 state="Cannot Connect"
                 try:
                    driver.find_element_by_xpath("//p[@class='alert alert-warning']//span[contains(text(), 'Incorrect username or password.')]")
                    connect=-1
                    state="Inc usr or passwd."
                 except:
                    connect=0
                 print(user_account +' > ' + state)
            except NoSuchElementException:
                 connect=1
        
            #if connected
            if(connect==1):
                print("connect : account " + user_account)
                #random ua 
                common.heart.random_ua(driver,'spoti')
                driver.switch_to.window("t2")
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
                   #get search input element
                   search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.inputBox-input")))
                   #fetch all songs 
                   for s in song:                
                    try:
                        if(opsy=='Linux'):
                          common.heart.clean_memory()
                        song_name = s[1]
                        song_duration = int(s[3])
                        song_artist = int(s[6])
                        song_artist_name = ""
                        #get artist of current song
                        for a in artists:
                             if(int(a[0]) == song_artist):
                                 song_artist_name = a[1] 

                        song_album = int(s[4])
                        song_album_url = ""
                        #get album of current song
                        for al in albums:
                             if(int(al[0]) == song_album):
                                 song_album_url = al[2] 
                                 song_album_url = song_album_url[24:] 
                                 song_album_name = al[1]
                        #put song + artist search input
                        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='navBar-expand']//li[2][@class='navBar-group']"))).click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='navBar-expand']//li[1][@class='navBar-group']"))).click()
                        search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.inputBox-input")))                  
                        search.send_keys(song_name + " " + song_artist_name)
                        try:
                           #wait until the result appears if not clean search input and put again other search X2 ## if not exit reload other
                           wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[contains(text(), '"+song_name+"')]")))
                        except :
                           driver.get("https://open.spotify.com/search/")
                           search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.inputBox-input")))                           
                           search.send_keys(song_name + " " + song_artist_name)
                           try:
                              wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[contains(text(), '"+song_name+"')]")))
                           except:
                              driver.get("https://open.spotify.com/search/")
                              search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.inputBox-input")))
                              search.send_keys(song_name + " " + song_artist_name)
                              try:
                                wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[contains(text(), '"+song_name+"')]")))
                              except :
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
                            men2 = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")               
                            # right click
                            ActionChains(driver).context_click(men2).perform() 
                            sleep(2) 
                            # save or skip
                            save = driver.find_element_by_xpath("//nav[@class='react-contextmenu react-contextmenu--visible']//div[2][@class='react-contextmenu-item']")
                            print(user_account + " > " + song_name + " " + save.text) 
                            if (("Sauvegarder" in save.text) or ("Save" in save.text) or ("Speichern" in save.text) or ("Guardar" in save.text) or ("Salva" in save.text) or ("Uložit"in save.text) or ("zapisać" in save.text)):
                                print(user_account + " > " + song_name + " " + save.text)
                                ActionChains(driver).move_to_element(save).perform() 
                                sleep(2)
                                cl = driver.find_element_by_xpath("//nav[@class='react-contextmenu react-contextmenu--visible']//div[2][@class='react-contextmenu-item react-contextmenu-item--selected']")                          						   
                                cl.click()
                                nn=1
                                sleep(2)

                            try:         
                                pplay = driver.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar__left']//div[@class='track-info ellipsis-one-line']//div[@class='track-info__name ellipsis-one-line']//div[@class='react-contextmenu-wrapper']").text 
                            except:
                                driver.refresh()
                                sleep(5)
                                try:
                                    pplay = driver.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar__left']//div[@class='track-info ellipsis-one-line']//div[@class='track-info__name ellipsis-one-line']//div[@class='react-contextmenu-wrapper']").text 
                                except:
                                     try:
                                       if(opsy=='Linux'):
                                           common.heart.kill_process(pid) 
                                       driver.close()
                                     except:
                                       err=1
                          except NoSuchElementException:
                            ppp='.'                                 
                    except:                                 
                        driver.refresh()                                 
                except StaleElementReferenceException:
                     sleep(1)          
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
                          

                # click track tab
                try:
                    a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/collection/tracks']")))
                    a.click()
                except:
                    try:
                        driver.refresh()
                        a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/collection/tracks']")))
                        a.click()
                    except:
                        driver.refresh()
                        a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/collection/tracks']")))
                        a.click()

                driver.execute_script("window.scrollBy(0, 1000);")
                sleep(5)
                driver.execute_script("window.scrollBy(0, 1000);")
                sleep(5)     
                driver.execute_script("window.scrollBy(0, 1000);")
                sleep(5)     
                ii=0
                pl=0
                nxt=0                
                for ss in song_s:
                    try:
                        driver.execute_script("window.scrollBy(0, 1000);")
                        sleep(5)
                        ii=ii+1
                        song_name = ss[1]
                        song_duration = int(ss[3])
                        song_album = int(ss[4])
                        song_album_url = ""
                        #get album of current song
                        for al in albums:
                             if(int(al[0]) == song_album):
                                 song_album_url = al[2] 
                                 song_album_url = song_album_url[24:] 
                                 song_album_name = al[1]
                        x=0
                        nn=0 
                        sleep(1)
                        try:
                           #wait until the result appears if not clean search input and put again other search X2 ## if not exit reload other
                           wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']")))
                        except:
                           try:
                              driver.refresh()
                              wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']")))
                           except:
                              
                              try:
                                driver.refresh()
                                wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']")))
                              except TimeoutException:
                                sleep(2)   
                        #change curent device to webdriver device 
                        heart.change_device(driver) 
                        #sleep(1)
                        #heart.change_device(driver)   

                        while((x<=50)and(nn<=0)):
                          try: 
                             x=x+1
                             txt = driver.find_element_by_xpath("//section[@class='tracklist-container']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[@class='tracklist-name']")
                             txt2 = driver.find_element_by_xpath("//section[@class='tracklist-container']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[@class='second-line ellipsis-one-line']//span[3]")
                             if(song_name.lower() == txt.text.lower() and txt2.text.lower()==song_album_name.lower()):
                               # find song and doubleclick
                               heart.doubleclick(driver,x,song_album_url)
                               sleep(5)
                               # if song state = pause or play = other song > replay
                               if(heart.replay(driver)==1):
                                  heart.doubleclick(driver,x,song_album_url)
                               if(pp%10==0):
                                  #ms=(random.randint(int(song_duration) - int(margin_play) , int(song_duration)))
                                  ms=(random.randint(30, 50))
                               else:
                                  ms=(random.randint(30, 50))                                                
                               print(user_account + " > Playing : " + song_name + " in " + str(ms) + " seconds")
                               pl=heart.player_(driver,song_name,ms,x,song_album_url,proxy_ip,user_account,cnx,ii) + pl
                               if(pl == 1 and nxt == 0):
                                   id_insert = common.heart.log_insert(proxy_ip,user_account,str(next_start),mypubilcip,"Save",cnx)
                                   nxt=1
                               elif pl > 1:
                                   #common.heart.log_update(pl,proxy_ip,user_account,cnx,'spoti')
                                   file = open("log/"+str(id_insert),"w") 
                                   file.write(str(pl))
                                   file.close()
                                   if(pl>=3):
                                     pl1=1

                               nn=1
                          except NoSuchElementException:
                            sleep(1)
                    except: 
                        sleep(5) 
                        driver.refresh()
      ##### exceptions 
      try:
         if(opsy=='Linux'):
            common.heart.kill_process(pid) 
         driver.close()
         common.heart.read_log_update(id_insert,cnx,'spoti','../spotify/log/')
      except:
         err=1
         common.heart.read_log_update(id_insert,cnx,'spoti','../spotify/log/')
      
      try:
         cnx = common.heart.connectiondb('spoti')
      except MySQLdb.Error as err:
         print("Error connection")
      if(connect == -1):  
         common.heart.error_account(user_account,password_account,cnx)
      if(connect_proxy != 1):        
         common.heart.error_proxy(in_use_proxy,id_proxy,cnx)
         common.heart.log_insert(proxy_ip,user_account,"Error proxy",mypubilcip,"Save",cnx)
      common.heart.finish(proxy_ip,user_account,cnx,state)     
      print(user_account + " > " + state)
    except MySQLdb.Error as err:
       print("----->Error connection")
       common.heart.read_log_update(id_insert,cnx,'spoti','../spotify/log/')
       err=1
   except :
      try:
       e = sys.exc_info()[0]
       print(str(e))
       if(opsy=='Linux'):
          common.heart.kill_process(pid) 
       driver.close()
       common.heart.read_log_update(id_insert,cnx,'spoti','../spotify/log/')
      except:
       err=1
       common.heart.read_log_update(id_insert,cnx,'spoti','../spotify/log/')
    
