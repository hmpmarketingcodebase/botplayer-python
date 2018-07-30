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
import platform
sys.path.append("..")
import common.heart

opsy = platform.system() #operation system (windows or linux)

if(opsy=='Linux'):
   #for server run with virtual display
   from pyvirtualdisplay import Display
   display = Display(visible=0, size=(1366, 768))
   display.start()
 

while(1): 
  try:
      sleep(15) 
#Connection
      cnx = common.heart.connectiondb('checker')

#get account
      account_=common.heart.select_account_geo(cnx)
      user_account = str(account_[1]) 
      password_account = str(account_[2])
      id_account = str(account_[0])
#country of account will be the same for proxy and user language
      country = str(account_[3])
     
#get proxy
      proxy = common.heart.proxis(country,cnx) 
      proxy_ip = str(proxy[1])
      #proxy_ip = ":"  
      id_proxy = str(proxy[0])       
    
#config webdriver
      driver = common.heart.config_driver()

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
                 except:
                    sleep(1)
          
      connect=1
      #check proxy connection
      if(connect_proxy==1):
            #login
            print("# Login : " + user_account + " - # Password : " + password_account)
            common.heart.login(driver,user_account,password_account)
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
                    common.heart.error_account(user_account,password_account,cnx)
                 except:
                    print("Errooor")
                    common.heart.valid_account(user_account,password_account,cnx)
                    connect=0
                 print(user_account +' > ' + state)
            except NoSuchElementException:
                 connect=1
        
            #if connected
            if(connect==1):
                print("connect : account " + user_account)
                #come back to default ua
                common.heart.random_ua(driver,'checker')
                driver.switch_to.window("t2")
                driver.get("https://www.spotify.com/us/account/overview/")
                driver.execute_script("window.scrollBy(0, 500);")
                count='all'
                try:
                   count = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'card-profile-country'))).text
                except:
                   err=1
                print("country is " + str(count))
                common.heart.account_geo(cnx,str(count),str(count),user_account,password_account,'checker')
            
      try:
         driver.close() 
      except :
         sleep(1)
  except:    
      print("error")
