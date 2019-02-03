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
from selenium.webdriver.support.select import Select
from random import choice 
import random
import sys
import MySQLdb
import datetime
import heart
from requests import get
from urllib.parse import quote
import platform
import heart
sys.path.append("..")
import common.heart

opsy = platform.system() #operation system (windows or linux)

if(opsy=='Linux'):
   #for server run with virtual display
   from pyvirtualdisplay import Display
   display = Display(visible=0, size=(1366, 768))
   display.start()
 

while(1):
      sleep(10)
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

      print(user_account + " > Let's Gooo!" )

#config webdriver
      driver = common.heart.config_driver()
#connect to proxy by extension, connexion browser side
      common.heart.proxy_connect(str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]),driver)
 
      common.heart.random_ua(driver,'deezer')
      driver.switch_to.window("t2")
         
      driver.get("https://www.deezer.com/login")
      connect_proxy=0

#check proxy state
      connect_proxy = heart.check_proxy(driver)
      if(connect_proxy == 0):
         state="Error Proxy!"            
      connect=1
      #check proxy connection
      if(connect_proxy==1):
            #login
            heart.login(driver,user_account,password_account)
            connect=-1
            try:
                 #if it's an invalid account then connect = 0
                 driver.find_element_by_xpath("//div[@id='login_error']")
                 state="Cannot Connect"
                 connect=-1
                 common.heart.error_account(user_account,password_account,cnx)
                 print(user_account +' > ' + state)
            except NoSuchElementException:
                 connect=1
        
            #if connected
            if(connect==1):
                print("connect : account " + user_account)
                url = "https://www.deezer.com/account"
                driver.get(url)
                sleep(5)
                city = driver.find_element_by_xpath("//input[@id='city']").text
                select = Select(driver.find_element_by_id('language'))
                count = select.first_selected_option
                country = str(count.text)[:2].lower()
                common.heart.account_geo(cnx,str(country),str(city),user_account,password_account,'deezer')
                print (count.text)
                print (city)
                print("#############################################")
      driver.close()