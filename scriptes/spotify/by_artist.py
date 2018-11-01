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
   
   
part = sys.argv[1] # 
part_sec = 86400 / int(part) # how many seconds in 1 part per day

opsy = platform.system() #operation system (windows or linux)

if(opsy=='Linux'):
   #for server run with virtual display
   from pyvirtualdisplay import Display
   display = Display(visible=0, size=(1366, 768))
   display.start()
#follow = 0
pid=10
while(1):
 #follow = follow + 1
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
  print("will be playing at :" + str(ttb) )
  sleep(tt)
  try: 
    try:
      id_insert = 0
      state="finish"
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

#get random common.heart.songs 
      x=[] 
      song = common.heart.songs(1,cnx)
      for s in song:
          x.append(s[1])  
#get albums
      albums = common.heart.albums_(cnx)
      
#get artist      
      artists = common.heart.artist(cnx)

#log insert (by search type)
      current=datetime.datetime.now()
      next_start = current

#common.heart.next_run(next_start,proxy_ip,user_account)
      #common.heart.log_insert(proxy_ip,user_account,str(next_start),"By Search",cnx)
      

#config webdriver
      driver = common.heart.config_driver('spoti','desktop')
      driver.service.process # is a Popen instance for the chromedriver process
      p = psutil.Process(driver.service.process.pid)
      print("#####################################")
      print ("PID : " + str(p.pid))      
      pid = str(p.pid)
#connect to proxy by extension, connexion browser side
      my = common.heart.proxy_connect(cnx,str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]),usr,pwd,driver,mypubilcip)
      myip = str(my).split(";")[0]
      mycountry = str(my).split(";")[1]
#get account
      account_=common.heart.account(cnx,mycountry)
      user_account = str(account_[1]) 
      password_account = str(account_[2])
      id_account = str(account_[0])
      print(user_account + " > Let's Gooo!" )
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
#Mobile user agent
      common.heart.mobile_ua(driver)
      
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
                   if(opsy=='Linux'):
                      common.heart.kill_process(pid) 
                   driver.close()
                 except:
                   err=1
      connect=1
      #check proxy connection
      if(connect_proxy==1):
            #heart.login
            heart.login(driver,user_account,password_account)
            connect=-1
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
                id_insert = common.heart.log_insert(str(proxy_ip),str(myip),user_account,str(next_start),mypubilcip,"Artist",cnx)
                file = open("log/"+str(id_insert),"w") 
                file.write(str(pl))
                file.close()
                print("connect : account " + user_account)
                #come back to default ua
                common.heart.default_ua(driver)
                driver.switch_to.window("t2")
                driver.get("https://open.spotify.com/browse/featured")
                #fetch all songs 
                ar=[1,2,3,4,5] 
                random.shuffle(ar)
                zz=0
                mm=0
                ss=int(ar[1])*5
                common.heart.check_ip(myip,driver)
                for a in artists:
                        follow=(random.randint(22, 1000))
                        if(opsy=='Linux'):
                           common.heart.clean_memory()
                        ii=ii+1
                        artist_url = a[2]
                        fol = a[3]
                        driver.get(artist_url)
                        f = follow%fol
                        print("follow = " +  str(f))
                        if(f == 0):
                        #if(1 == 1):
                           if(mm<ss ):
                            mm=mm+1
                            try:
                              try:
                                   
                                    # click search if not fin reload page X 2 if not exist quit and reload other
                                    a = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='header-buttons']//button[@class='btn btn-black btn--narrow']")))
                                    a.click() 
                                    sleep(5)  
                                
                              except TimeoutException:
                                    driver.get(artist_url)
                                    a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.spoticon-heart-24")))
                                    a.click() 
                                    sleep(5)  
                                
                            except TimeoutException:
                              try:
                                try:
                                    driver.get(artist_url)
                                    a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.spoticon-heart-24")))
                                    a.click() 
                                    sleep(5)  
                                
                                except TimeoutException:
                                    driver.get(artist_url)
                                    a = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='header-buttons']//button[@class='btn btn-black btn--narrow']")))
                                    a.click()
                                    sleep(5)  
                                
                              except TimeoutException:
                                driver.get(artist_url)
                                a = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='header-buttons']//button[@class='btn btn-black btn--narrow']")))
                                a.click()
                                sleep(5)  
                                
                        driver.execute_script("window.scrollBy(0, 1000);")
                        sleep(3)
                        zz=0
                        while(zz<5):
                          try:
                            print (ar)
                            kk=int(ar[zz])
                            zz=zz+1
                            try:
                                men = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(kk)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")
                            except:
                                driver.get(artist_url)
                                men = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(kk)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")
                            heart.change_device(driver)
                            sleep(2)
                            song_name = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(kk)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//div[@class='tracklist-name ellipsis-one-line']").text
                            if song_name in x:
                                ActionChains(driver).double_click(men).perform()
                                print("####### " + song_name)
                                ms=(random.randint(30, 40))
                                pl = heart.player_album(driver,song_name,ms,kk,proxy_ip,user_account,cnx,ii) + pl
                                if pl >= 1:
                                   #common.heart.log_update(pl,proxy_ip,user_account,cnx,'spoti')
                                   file = open("log/"+str(id_insert),"w") 
                                   file.write(str(pl))
                                   file.close()
                                
                          except:
                            sleep(1)
                        common.heart.check_ip(myip,driver)
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
         #common.heart.log_insert(proxy_ip,user_account,"Error proxy",mypubilcip,"Artist",cnx)
      print(state)
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
          