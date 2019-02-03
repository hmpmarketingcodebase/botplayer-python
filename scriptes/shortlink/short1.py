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

part = sys.argv[3] # 
part_sec = 86400 / int(part) # how many seconds in 1 part per- day
opsy = platform.system() #operation system (windows or linux)

if(opsy=='Linux'):
   #for server run with virtual display
   from pyvirtualdisplay import Display
   display = Display(visible=0, size=(1366, 768))
   display.start()

repeat=0
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
      pl=0
      id_insert = 0
      state="Finish"
      pp=pp+1
#Connection
      cnx = common.heart.connectiondb('spoti')

#get proxy
      #proxy = common.heart.proxis(cnx)
        
      proxy_ip = "usa.rotating.proxyrack.net:333"
      print(proxy_ip)
      #proxy_ip = ":" 
      #id_proxy = str(proxy[0])  
      usr = "corameleviv"       
      pwd = "anoualwifi10"       
      
	  

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
      if(my == "error proxy"):
            driver.close()         

      myip = str(my).split(";")[0]
      mycountry = str(my).split(";")[1]
      print("code country is : " + mycountry)

      print(myip + " ++ " + mycountry)

      print(" > Let's Goo!" )
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

      
      driver.get("http://destyy.com/wCnpiy")
     
      WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'skip_button'))).click()
      sleep(5)  
  except MySQLdb.Error as err:
      try:
          e = sys.exc_info()[0]
          print(str(e))
          if(opsy=='Linux'):
             common.heart.kill_process(pid) 
          driver.close()
          common.heart.log_update(str(id_insert),pl,'spoti')         
      except:
          err=1
          try:
             common.heart.log_update(str(id_insert),pl,'spoti')         
          except:
             err=1