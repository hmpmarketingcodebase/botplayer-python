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
import platform
import heart
import psutil
sys.path.append("..")
import common.heart
import os

#get public ip
try:
   mypubilcip = get('https://api.ipify.org').text
except:
   mypubilcip = "-"


margin_play = sys.argv[1] # margin play(duration of song = 120 seconds # margin play = 20 seconds # then play song between 100 and 120 seconds)
play_album_ = sys.argv[2] # id album(get from database)
part = sys.argv[3] # 
part_sec = 86400 / int(part) # how many seconds in 1 part per- day

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
  try:
       if(opsy=='Linux'):
          common.heart.kill_process(pid) 
       driver.close()
  except:
       err=1
  vv=vv+1  
  if(int(part_sec)<1):
      part_sec=2
  tt= int(random.randint(1,int(part_sec)))
  current=datetime.datetime.now()
  ttb = current + datetime.timedelta(0,tt)
  print("will be playing at :" + str(ttb) )
  sleep(tt)
  try: 
    try:
      id_insert = 0
      state="Finish"
      pp=pp+1
#Connection
      cnx = common.heart.connectiondb('spoti')

#get proxy
      proxy = common.heart.proxis(cnx) 
      proxy_ip = str(proxy[1])
      #proxy_ip = ":" 
      id_proxy = str(proxy[0])       
      usr = str(proxy[5])       
      pwd = str(proxy[6])       
      common.heart.proxy_in_use(id_proxy,cnx)

#get albums
      albums = common.heart.albums_(cnx)
      
#get playlist_album
      play_album = common.heart.playlist_album(str(play_album_),cnx)

#get artist      
      artists = common.heart.artist(cnx)

#log insert      
      current=datetime.datetime.now()
      next_start = current
      #common.heart.log_insert(proxy_ip,user_account,str(next_start),"By Album",cnx)

#config webdriver
      driver = common.heart.config_driver('spoti','desktop','x')
      driver.service.process # is a Popen instance for the chromedriver process
      p = psutil.Process(driver.service.process.pid)
      print("#####################################")
      print ("PID : " + str(p.pid))      
      pid = str(p.pid)
#connect to proxy by extension, connexion browser side
      my = common.heart.proxy_connect(cnx,str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]),usr,pwd,driver,mypubilcip,1)
      print(my)
      myip = str(my).split(";")[0]
      mycountry = str(my).split(";")[1]
      print("code country is : " + mycountry)
      if(mycountry.lower() not in ['jp','il','hk','id','my','ph','sg','tw','th','vn','ad','at','be','bg','cy','cz','dk','ee','fi','fr','de','gr','hu','is','ie','it','lv','li','lt','lu','mt','mc','nl','no','pl','pt','ro','sk','es','se','ch','tr','gb','ar','bo','br','cl','co','cr','do','ec','sv','gt','hn','mx','ni','pa','py','pe','uy','ca','us','za','au','nz','dz','bh','eg','jo','kw','lb','ma','om','ps','qa','sa','tn','ae']):
          driver.close()
      else:
          print("in")

      print(myip + " ++ " + mycountry)
#get account
      account_=common.heart.account(cnx,mycountry)
      user_account = str(account_[1]) 
      password_account = str(account_[2])
      id_account = str(account_[0])
#lang of account will be the same for proxy and user language
      #country = str(account_[3])
      common.heart.account_in_use(id_account,cnx) 
      print(user_account + " > Let's Goo!" )
      print("###### "  + str(myip) + " ######")
 
      #view current ip
      
      country = mycountry.lower()
      lang = mycountry.lower()
      if(country.lower() =='us' or country.lower() =='gb' or country.lower() =='ca' or country.lower() =='au' ):
          lang='en'
      if(country.lower() =='ar'):
          lang='es'
      print("language is " + lang)     
       
      common.heart.language_browser(lang,driver)
#Mobile user agent click extensions
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
        sleep(5)
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
           if(common.heart.proxy_used(myip,cnx,driver)) == 1:
              ii=0
              pl=0
              print("connect : account " + user_account)
              #come back to default ua 
              #common.heart.random_ua(driver,'spoti','desktop')
              common.heart.default_ua(driver)
              driver.switch_to.window("t2")
              #driver.get('http://www.whatsmyua.info/')
              #sleep(5)
              #driver.get('https://www.spotify.com/us/account/overview/?utm_source=play&utm_campaign=wwwredirect')
              #driver.execute_script("window.scrollBy(0, 500);")
              #sleep(10) 

              url = "https://open.spotify.com/browse/featured"
              driver.get(url)
              try:
                try:
                      wait = WebDriverWait(driver, 30)
                      # click search if not fin reload page X 2 if not exist quit and reload other
                      a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-subtle.navBar-link.ellipsis-one-line")))
                    
                except TimeoutException:
                      driver.get("https://open.spotify.com/browse/featured")
                      a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-subtle.navBar-link.ellipsis-one-line")))
              except TimeoutException:
                driver.get("https://open.spotify.com/browse/featured")
                a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-subtle.navBar-link.ellipsis-one-line")))

              for p_a in play_album:
               #get album of current play_album            
               for al in albums:
                try:
                  if(int(al[0]) == p_a[1]):
                     try:
                        cnx = common.heart.connectiondb('spoti')
                     except MySQLdb.Error as err:
                        print("Error connection")
                     song_album_url = al[2] 
                     song_album_name = al[1]
                     song = common.heart.songs_album(p_a[1],cnx)   
                     try:
                      try:
                          wait = WebDriverWait(driver, 30)
                          # click search if not fin reload page X 2 if not exist quit and reload other
                          a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-subtle.navBar-link.ellipsis-one-line")))
                         
                      except TimeoutException:
                          driver.get("https://open.spotify.com/browse/featured")
                          a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-subtle.navBar-link.ellipsis-one-line")))
                         
                     except TimeoutException:
                      driver.get("https://open.spotify.com/browse/featured")
                      a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-subtle.navBar-link.ellipsis-one-line")))
            
                     # search album
                     album_link = song_album_url
                     album_link =album_link[24:]
                     _link = album_link
                     album_artist = int(al[3])
                     for a in artists:
                        if(int(a[0]) == album_artist):
                            album_artist_name = a[1]
                     '''
                     wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='navBar-expand']//li[2][@class='navBar-group']"))).click()
                     wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='navBar-expand']//li[1][@class='navBar-group']"))).click()
                     search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.inputBox-input")))                  
                     search.send_keys(song_album_name + " " + album_artist_name)
                     sleep(5)
                     # click album tab
                     sl = driver.current_url
                     sl1 = sl.split('/')
                     sl = sl1[len(sl1)-1]
                     try:
                         a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/search/albums/"+str(sl)+"']")))
                         a.click()
                     except TimeoutException:
                         try:
                             print("album tab not found")
                             driver.refresh()
                             a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/search/albums/"+str(sl)+"']")))
                             a.click()
                         except TimeoutException:
                             driver.refresh()
                             a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/search/albums/"+str(sl)+"']")))
                             a.click()

                     try:
                      a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='mo-info-name' and @href='"+str(_link)+"']")))
                      a.click()
                     except TimeoutException:
                      driver.refresh()
                      a = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='mo-info-name' and @href='"+str(_link)+"']")))
                      a.click()
                     # wait result list
                     try:
                       wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']")))
                     except TimeoutException:
                       driver.refresh()
                       wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='tracklist-container']//div[1][@class='react-contextmenu-wrapper']")))
                     '''
                     driver.get(song_album_url)
                     sleep(1)
                     driver.execute_script("window.scrollBy(0, 1000);")
                     sleep(1)   
                     driver.execute_script("window.scrollBy(0, 1000);")
                     sleep(1)   
                     driver.execute_script("window.scrollBy(0, 1000);")
                     common.heart.check_ip(myip,driver)
                     for s in song:
                        try:
                         if(opsy=='Linux'):
                            common.heart.clean_memory()
                         ii=ii+1
                         song_name = s[1]
                         song_duration = int(s[3])
                         x=0
                         nn=0
                         #heart.change_device(driver)
                         #sleep(2)
                         heart.change_device(driver)
                         while((x<=20)and(nn<=0)):
                           try: 
                             x=x+1 
                             txt = driver.find_element_by_xpath("//section[@class='tracklist-container']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//div[@class='tracklist-name ellipsis-one-line']").text
                             print("find : " + txt)
                             if(song_name.lower() == txt.lower()):
                               nn=1
                               sleep(2)
                               # find and double click
                               heart.doubleclick_album(driver,x)
                               sleep(5)
                               if(heart.replay(driver)==1):
                                  heart.doubleclick_album(driver,x)
                               if(pp%10==0):
                                  #ms=(random.randint(int(song_duration) - int(margin_play) , int(song_duration)))
                                  ms=(random.randint(30, 50))                                                
                               else:
                                  ms=(random.randint(30, 50))                                                
                               print(user_account + " > Playing : " + song_name + " in " + str(ms) + " seconds")
                               pl = heart.player_album(driver,song_name,ms,x,proxy_ip,user_account,cnx,ii) + pl
                               if pl > 1:
                                   #common.heart.log_update(pl,proxy_ip,user_account,cnx,'spoti')
                                   file = open("log/"+str(id_insert),"w") 
                                   file.write(str(pl))
                                   file.close()
                               if(pl == 1):
                                    common.heart.error_proxy(id_proxy,cnx)
                                    id_insert = common.heart.log_insert(str(proxy_ip),str(myip),user_account,str(next_start),mypubilcip,"Album",cnx)
                                    common.heart.proxy_used_id(myip,cnx,driver,id_insert)
                                    file = open("log/"+str(id_insert),"w") 
                                    file.write(str(pl))
                                    file.close()
                               print("------> " + str(pl))
                               
                           except NoSuchElementException:
                               if(x<4):
                                 driver.refresh()
                         
                        except: 
                            driver.refresh()
                        common.heart.check_ip(myip,driver)
                except: 
                    driver.refresh() 
                    
      ##### exceptions 
      
      try:
          if(opsy=='Linux'):
             common.heart.kill_process(pid) 
          driver.close()
          common.heart.read_log_update(id_insert,'spoti','../spotify/log/')
      except:
          err=1
          common.heart.read_log_update(id_insert,'spoti','../spotify/log/')
      
      try:
         cnx = common.heart.connectiondb('spoti')
      except MySQLdb.Error as err:
         print("Error connection")
      if(connect == -1):  
         common.heart.error_account(user_account,password_account,cnx)
      #if(connect_proxy != 1):        
         #common.heart.error_proxy(in_use_proxy,id_proxy,cnx)
         #id_insert = common.heart.log_insert(str(proxy_ip),str(myip),user_account,"Error proxy",mypubilcip,"Album",cnx)
      #common.heart.finish(proxy_ip,user_account,cnx,state)     
      print(user_account + " > " + state)
    except MySQLdb.Error as err:
       print("----->Error connection")
       common.heart.read_log_update(id_insert,'spoti','../spotify/log/')
  except :
      try:
          e = sys.exc_info()[0]
          print(str(e))
          if(opsy=='Linux'):
             common.heart.kill_process(pid) 
          driver.close()
          common.heart.read_log_update(id_insert,'spoti','../spotify/log/')
      except:
          err=1
  