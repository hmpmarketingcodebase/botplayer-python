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
follow = 199
pid=10
while(1):
 follow = follow + 1
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
   #try: 
    #try:
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
      #common.heart.random_ua(driver,'deezer')
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
                    driver.find_element_by_xpath("//div[@id='notify']//a[2]").click()
                    print('New Version')
                except:
                    print("--")
                ii=0
                pl=0
                insert=0
                for a in artists:
                        id_artist = a[0]
                        song = common.heart.songs_artist(id_artist,cnx)
                        if(opsy=='Linux'):
                           common.heart.clean_memory()
                        ii=ii+1
                        artist_url = a[2]
                        driver.get(artist_url+"/top_track")
                        heart.right_search_and_play(driver,song,artists,albums,"artist",proxy_ip,user_account,next_start,mypubilcip,cnx)                    
                    
      ##### exceptions 
      try:
         if(opsy=='Linux'):
            common.heart.kill_process(pid) 
         driver.close()
      except:
          err=1
      
      try:
         cnx = common.heart.connectiondb('deezer')
      except MySQLdb.Error as err:
         print("Error connection")
      if(connect == -1):  
         common.heart.error_account(user_account,password_account,cnx)
      if(connect_proxy != 1):        
         common.heart.error_proxy(in_use_proxy,id_proxy,cnx)
         common.heart.log_insert(proxy_ip,user_account,"Error proxy",mypubilcip,"Artist",cnx)
      print(state)
      common.heart.finish(proxy_ip,user_account,cnx,state)     
      print(user_account + " > " + state)
