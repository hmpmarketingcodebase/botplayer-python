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

playlist = sys.argv[1] # id album(get from database)
playlist_account = sys.argv[2] # id album(get from database)
proxy_number = sys.argv[3]
level = sys.argv[4]
database = 'spoti' # 
#ip_prox = sys.argv[4] # 
#min = sys.argv[5] # 
#max = sys.argv[6] # 
part = 1000000
part_sec = 86400 / int(part) # how many seconds in 1 part per- day
#prt = int(sys.argv[4])
opsy = platform.system() #operation system (windows or linux)
#35.185.98.205
 
proxy_ = ["163.172.39.13","163.172.39.13","51.15.13.157","51.15.13.157","209.205.212.34"]
port_start =[1151,1163,3226,3239,3000]
port_end =[1162,1175,3238,3250,3250]

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
       #if(opsy=='Linux'):
       print("KILLL " + str(pid))
       common.heart.kill_process(driver) 
       print("KILLLED " + str(pid)) 
       driver.close()
       driver.close()
       driver.close()
  except:
       err=1
  pos_ = int(proxy_number)
  pos_ = pos_-1
  min = port_start[pos_]
  max = port_end[pos_]
  ip_prox = proxy_[pos_]
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
    try:  
     try:
      pl=0
      plc=0
      aaa=0
      id_insert = 0
      state="Finish"
      pp=pp+1
#Connection
      cnx = common.heart.connectiondb(database)

#get proxy
      #proxy = common.heart.proxis(cnx)
      #prt = int(random.randint(9177,9476))       
      prt = int(random.randint(int(min),int(max)))       
      #proxy_ip = "195.154.161.111:"+str(prt)
      proxy_ip = str(ip_prox)+":"+str(prt)
      print(proxy_ip)
      #proxy_ip = ":" 
      #id_proxy = str(proxy[0])  
      usr = "corameleviv"       
      pwd = "anoualwifi10"       
      #common.heart.proxy_in_use(id_proxy,cnx)

#log insert      
      current=datetime.datetime.now()
      next_start = current
      #common.heart.log_insert(proxy_ip,user_account,str(next_start),"By Album",cnx)

#config webdriver
      driver = common.heart.config_driver(database,'mobile','x')
      driver.service.process # is a Popen instance for the chromedriver process
      p = psutil.Process(driver.service.process.pid)
      print("#####################################")
      print ("PID : " + str(p.pid))      
      pid = str(p.pid)
#connect to proxy by extension, connexion browser side
      my = common.heart.proxy_connect(cnx,str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]),usr,pwd,driver,mypubilcip,"Mobile",playlist)
      print(my)
      if(my == "error proxy"):
            driver.close()         

      myip = str(my).split(";")[0]
      mycountry = str(my).split(";")[1]
      print("code country is : " + mycountry)
      if(mycountry.lower() not in ['jp','il','hk','id','my','ph','sg','tw','th','vn','ad','at','be','bg','cy','cz','dk','ee','fi','fr','de','gr','hu','is','ie','it','lv','li','lt','lu','mt','mc','nl','no','pl','pt','ro','sk','es','se','ch','tr','gb','ar','bo','br','cl','co','cr','do','ec','sv','gt','hn','mx','ni','pa','py','pe','uy','ca','us','za','au','nz','dz','bh','eg','jo','kw','lb','ma','om','ps','qa','sa','tn','ae']):
          print('not in')
          driver.close()
      else:
          print("in")

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
#Mobile user agent click extensions
      common.heart.mobile_ua(driver)
      
      driver.get("https://accounts.spotify.com/en/login")
      connect_proxy=0

#if authentication successfully then connect_proxy = 1 and continue ## if not reload by other proxy
      try:
          WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login-username')))
          print (" > Proxy is ready!")
          connect_proxy=1
      except TimeoutException:
          try:
              driver.get("https://accounts.spotify.com/en/login")
              WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login-username')))
              print (" > Proxy is ready!")
              connect_proxy=1
          except TimeoutException:
              print (" > Loading took too much time! (proxy)")
              connect_proxy=0
              state="Error Proxy!" 
      connect=0
      
      #check proxy connection
      if(connect_proxy==1):
        ll=0
        #login
        while(connect != 1 and ll<10):
          #get account
          ll=ll+1
          account_=common.heart.account(cnx,mycountry,playlist_account)
          #print("ddddddd  " + account_)
          user_account = str(account_[1])
          password_account = str(account_[2])
          id_account = str(account_[0])
          #lang of account will be the same for proxy and user language
          #country = str(account_[3])
          
          if(ll>1):
             driver.get("https://accounts.spotify.com/en/login")
          common.heart.login(driver,user_account,password_account)
          sleep(5)
          connect=1 
          try:
             driver.find_element_by_xpath("//button[@class='btn btn-block btn-green ng-binding ng-scope']")
          except:
             connect=-1
             state="Inc usr or passwd."
             common.heart.error_account(user_account,password_account,cnx)
                          
        #if connected
        if(connect==1):
           if(common.heart.proxy_used(myip,cnx,driver,playlist)) == 1:
                     ii=0    
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

                     ins = 0
              
                     song = common.heart.songs_direct_mobile(playlist,playlist_account,level,cnx)   
                     
                     for s in song:
                        try:
                         driver.get(s[2])
                         plc=0
                         try:
                            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'Button__button-hJkQuQ') and contains(@class,'iJmjgq')]"))) 
                            print("staart")
                            try:
                               driver.find_element_by_xpath("//button[contains(@class,'sc-htpNat') and contains(@class,'jbRVWE') and contains(@class,'Button__button-hJkQuQ iJmjgq') and contains(@class,'iJmjgq')]")
                               print("other user play by this account we will quit")                         
                               driver.close()
                               driver.close()
                            except:                         
                               err=1                         
                            men = driver.find_element_by_xpath("//button[contains(@class,'Button__button-hJkQuQ') and contains(@class,'iJmjgq')]//span[contains(@class,'Metronome-ciQILY') and contains(@class,'gniMpK') and contains(@class,'Type-eNuXDw') and contains(@class,'hAKccv') ]")
                            men.click()
                            print("plaay")
                            sleep(5)
                            try:
                               driver.find_element_by_xpath("//button[contains(@class,'NowPlayingView__StyledHeartButton-eexIXf') and contains(@class,'cUQarj') and contains(@class,'ButtonReset-ewWVwp') and contains(@class,'jKBnzf')]").click()
                            except:
                               err=0
                            pp=10
                            if(pp%10==0):
                                  #ms=(random.randint(int(song_duration) - int(margin_play) , int(song_duration)))
                                  ms=(random.randint(40, 60))                                                
                            else:
                                  ms=(random.randint(40, 60))  
                            sleep(ms)
                            aaa=1
                            pl = aaa + pl
                            plc = aaa + plc
                            if(pl == 1 and ins ==0):
                                    ins+= 1
                                    #common.heart.error_proxy(id_proxy,cnx)
                                    id_insert = common.heart.log_insert(str(proxy_ip),str(myip),user_account,str(next_start),mypubilcip,"Mobile",playlist,playlist_account,cnx)
                                    print("inserted row = " + str(id_insert))
                                    repeat = 0
                                    common.heart.proxy_used_id(myip,cnx,driver,id_insert,playlist,'Mobile')
                            print("------> " + str(pl))
                         except:
                            err=1
                         #sleep(1000)
                        except: 
                            driver.refresh()
                        common.heart.check_ip(myip,driver)
                     sleep(15)
 
                    
      ##### exceptions 
      try:
          if(opsy=='Linux'):
             common.heart.kill_process(driver) 
          driver.close()
          common.heart.log_update(str(id_insert),pl,database)         
      except:
          err=1
          common.heart.log_update(str(id_insert),pl,database)         
        
      try:
         cnx = common.heart.connectiondb(database)
      except MySQLdb.Error as err:
         print("Error connection")
      
      #if(connect_proxy != 1):        
         #common.heart.error_proxy(in_use_proxy,id_proxy,cnx)
         #id_insert = common.heart.log_insert(str(proxy_ip),str(myip),user_account,"Error proxy",mypubilcip,"Album",cnx)
      #common.heart.finish(proxy_ip,user_account,cnx,state)     
      print(user_account + " > " + state)
     except MySQLdb.Error as err:
       print("----->Error connection")
       
    except  TimeoutException:
      try:
          e = sys.exc_info()[0]
          print(str(e))
          if(opsy=='Linux'):
             common.heart.kill_process(driver) 
          driver.close()
          common.heart.log_update(str(id_insert),pl,database)         
      except TimeoutException:
          err=1
          try:
             common.heart.log_update(str(id_insert),pl,database)         
          except:
             err=1
   except TimeoutException:
     print("skip1")
  except TimeoutException:
   print("skip2")  