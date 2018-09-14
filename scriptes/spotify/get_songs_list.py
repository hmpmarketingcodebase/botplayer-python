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
import csv

opsy = platform.system() #operation system (windows or linux)

if(opsy=='Linux'):
   #for server run with virtual display
   from pyvirtualdisplay import Display
   display = Display(visible=0, size=(1366, 768))
   display.start()
   
cnx = common.heart.connectiondb('spoti')
account_=common.heart.account(cnx)
user_account = str(account_[1]) 
password_account = str(account_[2])
 
#get albums
albums = common.heart.albums_(cnx)
      
driver = common.heart.config_driver()
common.heart.mobile_ua(driver)
driver.get("https://accounts.spotify.com/en/login")
connect_proxy=0
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
              
              print("connect : account " + user_account)
              #come back to default ua 
              common.heart.random_ua(driver,'spoti')
              driver.switch_to.window("t2")
              #driver.get('http://www.whatsmyua.info/')
              #sleep(5)
              #driver.get('https://www.spotify.com/us/account/overview/?utm_source=play&utm_campaign=wwwredirect')
              #driver.execute_script("window.scrollBy(0, 500);")
              #sleep(10) 
              url = "https://open.spotify.com/browse/featured"
              # driver.get(url)
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
                a.click()

              ii=0
              pl=0
              nxt=0
              for al in albums:
                try:
                     fields=["----","----","----"]
                     with open('out.csv', 'a',newline='') as f:
                        writer = csv.writer(f, delimiter = ';')
                        writer.writerow(fields)                     
                     try:
                        cnx = common.heart.connectiondb('spoti')
                     except MySQLdb.Error as err:
                        print("Error connection")
                     song_album_url = al[2] 
                     song_album_name = al[1]
                     
                     driver.get(song_album_url)
                     driver.execute_script("window.scrollBy(0, 1000);")
                     sleep(1)
                     driver.execute_script("window.scrollBy(0, 1000);")
                     sleep(1)     
                     driver.execute_script("window.scrollBy(0, 1000);")
                     sleep(1)     
                     artist = driver.find_element_by_xpath("//div[@class='col-xs-12 col-lg-3 col-xl-4 col-sticky']//header[@class='entity-info']//div[@class='media-object']//div[@class='mo-meta ellipsis-one-line']//div[@class='react-contextmenu-wrapper']")
                     artist_link = driver.find_element_by_xpath("//div[@class='col-xs-12 col-lg-3 col-xl-4 col-sticky']//header[@class='entity-info']//div[@class='media-object']//div[@class='mo-meta ellipsis-one-line']//div[@class='react-contextmenu-wrapper']//a")
                     album_name_ = driver.find_element_by_xpath("//div[@class='col-xs-12 col-lg-3 col-xl-4 col-sticky']//header[@class='entity-info']//div[@class='media-object']//div[@class='media-object-hoverable']//div[@class='mo-info']//div[@class='react-contextmenu-wrapper']//div[@class='mo-info-name']")
                     print ("artist is :" + artist.text)
                     print ("artist link is :" + str(artist_link.get_attribute("href")))
                     print ("album is :" + album_name_.text)
                     fields=[artist.text,"artist",str(artist_link.get_attribute("href"))]
                     with open('out.csv', 'a',newline='') as f:
                        writer = csv.writer(f, delimiter = ';')
                        writer.writerow(fields)
                     aaa = artist.text  
                     fields=[artist.text,album_name_.text,song_album_url]
                     with open('out.csv', 'a',newline='') as f:
                        writer = csv.writer(f, delimiter = ';')
                        writer.writerow(fields)


                     try:
                        for x in range(1,100): 
                             song_name_ = driver.find_element_by_xpath("//section[@class='tracklist-container']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[@class='tracklist-name']")
                             print("Song name : " + song_name_.text)                             
                             ActionChains(driver).context_click(song_name_).perform() 
                             sleep(3)
                             link = driver.find_element_by_xpath("//nav[@class='react-contextmenu react-contextmenu--visible']//div[5][@class='react-contextmenu-item']//textarea")
                             print(user_account + " > " + link.get_attribute("value")) 
                             sleep(3)
                             fields=[aaa,song_name_.text,link.get_attribute("value")]
                             with open('out.csv', 'a',newline='') as f:
                               writer = csv.writer(f, delimiter = ';')
                               writer.writerow(fields)
                             sleep(3)
                             driver.refresh()
                             driver.execute_script("window.scrollBy(0, 1000);")
                             sleep(1)
                             driver.execute_script("window.scrollBy(0, 1000);")
                             sleep(1)     
                             driver.execute_script("window.scrollBy(0, 1000);")
                             sleep(1)                                  
                     except NoSuchElementException:
                               print("-")
                except: 
                    print("******")