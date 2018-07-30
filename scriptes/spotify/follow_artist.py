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
follow=0
k=0
while(follow<1 and k < 10):
   try: 
    try: 
      k=k+1
#Connection
      cnx = common.heart.connectiondb('spoti')

#get proxy
      proxy = common.heart.proxis(1,cnx)
      #proxy_ip = str(proxy[1])
      proxy_ip = ":"  
      id_proxy = str(proxy[0])       

#get account
      account_=common.heart.account(1,cnx)
      user_account = str(account_[1]) 
      password_account = str(account_[2])

#get artist      
      artist = heart.artist(cnx)

#config webdriver
      driver = common.heart.config_driver()
      
#connect to proxy by extension, connexion browser side
      common.heart.common.heart.proxy_connect(str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]),driver)
 
      #view current ip
      #driver.get("http://www.mon-ip.com/info-adresse-ip.php")

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
             heart.login(driver,user_account,password_account)
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
              print("connect : account " + user_account)
              #come back to default ua 
              common.heart.random_ua(driver,'spoti')
              driver.switch_to.window("t2")
              url = artist[2]
              driver.get(url)
              try:
                try:
                      wait = WebDriverWait(driver, 30)
                      # click search if not fin reload page X 2 if not exist quit and reload other
                      a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.spoticon-heart-24")))
                      a.click()
                      sleep(5)  
                      print('save ' + artist[1] + ' to library')
                      follow = 1
                except TimeoutException:
                      driver.get(url)
                      a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.spoticon-heart-24")))
                      a.click() 
                      sleep(5)  
                      print('save ' + artist[1] + ' to library') 
                      follow = 1
              except TimeoutException:
                try:
                  try:
                      driver.get(url)
                      # click search if not fin reload page X 2 if not exist quit and reload other
                      a = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='header-buttons']//button[@class='btn btn-black btn--narrow']")))
                      a.click() 
                      sleep(5)  
                      print('>> save ' + artist[1] + ' to library')
                      follow = 1
                  except TimeoutException:
                      driver.get(url)
                      a = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='header-buttons']//button[@class='btn btn-black btn--narrow']")))
                      a.click()
                      sleep(5)  
                      print('save ' + artist[1] + ' to library') 
                      follow = 1
                except TimeoutException:
                  driver.get(url)
                  a = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='header-buttons']//button[@class='btn btn-black btn--narrow']")))
                  a.click()
                  sleep(5)  
                  print('save ' + artist[1] + ' to library')
                  follow = 1

  
      ##### exceptions 
      try:
         driver.close() 
      except :
         sleep(1)      
    except MySQLdb.Error as err:
       print("----->Error connection")
   except :
      print("error")
      try:
         driver.close() 
      except:    
         sleep(1)
