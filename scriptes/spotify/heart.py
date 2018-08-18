import os
from os import path 
import MySQLdb
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# replay if pause
def replay(driver):
    try:
       play = driver.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar']//div[@class='now-playing-bar__center']//div[@class='player-controls__buttons']//button[@class='control-button spoticon-pause-16 control-button--circled']")           
       return 0        
    except NoSuchElementException:
       return 1

def doubleclick(driver,x,song_album_url):
    try:  
       txt = driver.find_element_by_xpath("//section[@class='tracklist-container']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']//span[@class='second-line ellipsis-one-line']")
       print("find : " + txt.text)
       men = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")
       ActionChains(driver).move_to_element(men).perform()                    
       sleep(2)
       men2 = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")               
       ActionChains(driver).double_click(men2).perform() 
    except NoSuchElementException:
       print("-")

def doubleclick_album(driver,x):
    try:
       
       men = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']")
       ActionChains(driver).move_to_element(men).perform()
       sleep(3)
       driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       try:
           driver.execute_script("window.scrollBy(0, 500);")
           men2 = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']")               
           ActionChains(driver).double_click(men2).perform() 						  
                     
       except NoSuchElementException:
           driver.execute_script("window.scrollBy(0, -500);")
           men2 = driver.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col name']")
           ActionChains(driver).double_click(men2).perform()                
    except NoSuchElementException:
           sleep(1)

 
def player_(d,song_name,ms,x,song_album_url,proxy_ip,user_account,cnx,ii):
    try:
       sl = int(ms / 5)
       f=0
       i=0
       m=0
       pl=0
       pplay=""
       while(f<=sl):
         f=f+1 
         sleep(5)
         try:         
            pplay = d.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar__left']//div[@class='track-info ellipsis-one-line']//div[@class='track-info__name ellipsis-one-line']//div[@class='react-contextmenu-wrapper']").text 

         except:
            d.refresh()
            sleep(5)
            try:
                pplay = d.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar__left']//div[@class='track-info ellipsis-one-line']//div[@class='track-info__name ellipsis-one-line']//div[@class='react-contextmenu-wrapper']").text 
            except:
                try:
                   d.close() 
                except:
                   sleep(1)
           
         if(pplay != song_name):
           m=m+1
           print(song_name + " ^ "+ pplay)
           change_device(d)
           sleep(1)
           men = d.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")
           ActionChains(d).move_to_element(men).perform()                    
           sleep(1)
           men2 = d.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")               
           ActionChains(d).double_click(men2).perform()
           print("replay")
           if(m==3):
              d.refresh()
         else:
           m=m-1
           if(replay(d)==1):
              print("playing >")
              doubleclick(d,x,song_album_url)
              i=i-1
              if(i==-2):
                 d.refresh()
              sleep(5)
           else:
              i=i+1
              iii=ii*i
              if(i==6):
                  print("yeah !!")
                  pl=1
                  #log_update(str(ii),str(iii),proxy_ip,user_account,cnx)                                    
    except :
           sleep(1)
    return(pl)

# check if play is running 

def player_album(d,song_name,ms,x,proxy_ip,user_account,cnx,ii):
    try:
       sl = int(ms / 5)
       f=0
       i=0
       m=0
       pl=0
       pplay="" 
       while(f<=sl):
         f=f+1 
         sleep(5)
         try:         
            pplay = d.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar__left']//div[@class='track-info ellipsis-one-line']//div[@class='track-info__name ellipsis-one-line']//div[@class='react-contextmenu-wrapper']").text 
         except:
            d.refresh()
            try:
                pplay = d.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar__left']//div[@class='track-info ellipsis-one-line']//div[@class='track-info__name ellipsis-one-line']//div[@class='react-contextmenu-wrapper']").text 
            except:
                d.close() 
         if(pplay != song_name):
           print("> "+ pplay);
           change_device(d)
           sleep(1)
           men = d.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")
           ActionChains(d).move_to_element(men).perform()                    
           sleep(1)
           men2 = d.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")               
           ActionChains(d).double_click(men2).perform()
           print("replay")
           m=m+1
           if(m==3):
              d.refresh()
         else:
           m=m-1
           if(replay(d)==1):
              doubleclick_album(d,x)
              i=i-1
              if(i==2):
                 d.refresh()
              sleep(5)
           else:
              print("playing >")
              i=i+1
              iii=ii*i
              if(i==6):
                  print("yeaah!! ")
                  #log_update(str(ii),str(iii),proxy_ip,user_account,cnx)                                    
                  pl=1
    except NoSuchElementException:
           sleep(1)
    return pl
#change device
def change_device(d):
    try:       

        web_device=d.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar']//div[@class='now-playing-bar__right']//div[@class='now-playing-bar__right__inner']//span[@class='connect-device-picker']")
        web_device.click()
        sleep(2) 
        web_device_current=d.find_element_by_xpath("//footer[@class='now-playing-bar-container']//div[@class='now-playing-bar']//div[@class='now-playing-bar__right']//div[@class='now-playing-bar__right__inner']//span[@class='connect-device-picker']//div[@class='connect-device-list-container connect-device-list-container--is-visible']//div[@class='connect-device-list-content']//button[1]")
        web_device_current.click()
           
    except NoSuchElementException:
        print("Device Not found")


def login(driver,user_account,password_account):
    
    try:
       driver.find_element_by_xpath("//input[@id='login-username']").send_keys(user_account)
       driver.find_element_by_xpath("//input[@id='login-password']").send_keys(password_account)
       driver.find_element_by_xpath("//button[@id='login-button']").click()
       sleep(5)
    except NoSuchElementException:
       driver.close()


def killed_account(user_account,cnx):
    try:  
        cursor = cnx.cursor()
        cmd="UPDATE `account` SET `error`=4 WHERE `user`='"+user_account+"' "
        print(cmd)
        cursor.execute(cmd)
        cnx.commit() 
    except MySQLdb.Error as err:
        print("Something went wrong: (connection) {}".format(err))

