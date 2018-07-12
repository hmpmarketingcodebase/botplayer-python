import os
from os import path
import MySQLdb
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import datetime

def connectiondb():
   cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.","spoti")    
   return cnx
   

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

# check if play is running 
def player_(d,song_name,ms,x,song_album_url,proxy_ip,user_account,cnx,ii):
    try:
       sl = int(ms / 5)
       f=0
       i=0

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
                killed_account(user_account)
                d.close() 
             
           
         if(pplay != song_name):
           print(song_name + " ^ "+ pplay)
           change_device(d)
           sleep(1)
           men = d.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")
           ActionChains(d).move_to_element(men).perform()                    
           sleep(1)
           men2 = d.find_element_by_xpath("//ol[@class='tracklist']//div["+str(x)+"][@class='react-contextmenu-wrapper']//div[@class='tracklist-col position-outer']")               
           ActionChains(d).double_click(men2).perform()
           print("replay")
         else:
           if(replay(d)==1):
              print("playing >")
              doubleclick(d,x,song_album_url)
              i=i-1
              sleep(5)
           else:
              i=i+1
              iii=ii*i
              if(i==3):
                  print("yeah !!")
                  log_update(str(ii),str(iii),proxy_ip,user_account,cnx)                                    
    except NoSuchElementException:
           sleep(1)


# check if play is running 

def player_album(d,song_name,ms,x,proxy_ip,user_account,cnx,ii):
    try:
       sl = int(ms / 5)
       f=0
       i=0
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
         else:
           if(replay(d)==1):
              doubleclick_album(d,x)
              i=i-1
              sleep(5)
           else:
              print("playing >")
              i=i+1
              iii=ii*i
              if(i==3):
                  print("yeaah!! " + str(i))
                  log_update(str(ii),str(iii),proxy_ip,user_account,cnx)                                    
    except NoSuchElementException:
           sleep(1)

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



def proxis(country,cnx):
      try:
         curs = cnx.cursor()
         if(country == "1"):
           curs .execute("select * from proxies  where error <> 1 order by in_use asc, RAND()")  
         else:
           curs.execute("select * from proxies where error <> 1 and country=" + str(country) + " order by in_use asc, RAND()")  
         proxy = curs.fetchone() 
         return proxy
      except MySQLdb.Error as err:  
         print("Something went wrong: (proxies select) {}".format(err))   


def proxy_in_use(in_use_proxy,id_proxy,cnx):
    try:
         curs = cnx.cursor()
         in_use = int(in_use_proxy) + 1
         curs.execute("UPDATE proxies SET in_use = " + str(in_use) + " WHERE id = "+ str(id_proxy) )
         cnx.commit() 
    except MySQLdb.Error as err:
         print("Something went wrong: (Proxies update) {}".format(err))

def account(country,cnx):
      try:
         curs = cnx.cursor()
         if(country == "1"):
           curs.execute("select * from account where error = 2 order by in_use asc, RAND()")  
         else:
           curs.execute("select * from account  where error = 2 and country=" + str(country) + " order by in_use asc, RAND()")  
         account = curs.fetchone() 
         return account
      except MySQLdb.Error as err:  
         print("Something went wrong: (Accounts) {}".format(err))   


def account_in_use(in_use_account,id_account,cnx):
      try:
         
         curs = cnx.cursor()
         in_use = int(in_use_account) + 1
         curs.execute("UPDATE account SET in_use = " + str(in_use) + " WHERE id = "+ str(id_account) )
         cnx.commit() 
      except MySQLdb.Error as err:
         print("Something went wrong: {}".format(err))

def songs(id_playlist,cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from songs where playlist = '" + str(id_playlist) + "' order by RAND()")
         songs = curs.fetchall()
         return songs
      except MySQLdb.Error as err:  
         print("Something went wrong: (song) {}".format(err)) 


def songs_album(id_album,cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from songs where album = '" + str(id_album) + "' order by RAND()")
         songs = curs.fetchall()
         return songs
      except MySQLdb.Error as err:  
         print("Something went wrong: (song) {}".format(err)) 


def playlist_album(play_album,cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from playlist_album where play = " + str(int(play_album)) + " order by RAND()")
         songs = curs.fetchall()
         return songs
      except MySQLdb.Error as err:  
         print("Something went wrong: (song) {}".format(err)) 

def albums_(cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from album")
         albums = curs.fetchall()
         return albums
      except MySQLdb.Error as err:  
         print("Something went wrong: (album) {}".format(err)) 

def artist(cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from artist")
         artists = curs.fetchall()
         return artists
      except MySQLdb.Error as err:  
         print("Something went wrong: (artists) {}".format(err))   

def log_insert(proxy_ip,user_account,next_start,type_,cnx):
      try:
         curs = cnx.cursor()
         curs.execute("INSERT INTO `log`(`proxy`, `account`, `next_start`, `number_play`, `songs`, `seconds`, `type`) VALUES ('"+proxy_ip+"','"+user_account+"','"+next_start+"',0,0,0,'"+type_+"')")
         cnx.commit() 
      except MySQLdb.Error as err:  
         print("Something went wrong: (by search) {}".format(err))  

def log_update(rep,sng,proxy_ip,user_account,cnx):
      try:          
          cnx = connectiondb()
          cursor = cnx.cursor()               
          cursor.execute("UPDATE `log` SET `number_play`="+str(rep)+",`songs`='"+ str(sng) +"'  WHERE `proxy` = '"+proxy_ip+"' and `account` = '" +user_account+ "' ")
          cnx.commit()  
      except MySQLdb.Error as err:  
          print("Something went wrong: (search) {}".format(err))   
 
 

def next_run(next_start,proxy_ip,user_account):
         try:          
            cnx = connectiondb()
            curs = cnx.cursor()               
            curs.execute("UPDATE `log` SET `next_start`='"+str(next_start)+"' WHERE `proxy` = '"+proxy_ip+"' and `account` = '" +user_account+ "' ")
            cnx.commit()  
         except MySQLdb.Error as err:  
            print("Something went wrong: (search) {}".format(err))   

def config_driver(os):
 if (os=='linux'):
  try:
    #print(path.dirname(path.abspath(__file__)))
    direct = (path.abspath(path.join(path.dirname( __file__ ), '..', 'tools')))
    executable_path = direct + "/chromedriver"
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_extension(direct+'/Chrome-proxy-helper-master.crx')
    chrome_options.add_extension(direct+ '/extension_2_0_0_0.crx')
    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    return driver  
  except ConnectionResetError:
    sleep(1)
    print("linux error")
 elif (os=='windows'):
  try:
    
    executable_path = "tools/chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_extension('tools/Chrome-proxy-helper-master.crx')
    chrome_options.add_extension('tools/extension_2_0_0_0.crx')
    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    return driver  
  except ConnectionResetError:
    sleep(1)
    print("linux error")
def mobile_ua(driver):
     #Mobile user agent click extension
     driver.get("chrome-extension://lkmofgnohbedopheiphabfhfjgkhfcgf/popup.html")
     driver.execute_script("window.open('https://accounts.spotify.com/en/login', 'window')")
     try:
         driver.find_element_by_xpath("//a[@id='iPad']").click()
     except NoSuchElementException:
         print("NoSuchElementException : User agent Mobile") 
    #end Mobile user agent click extension
     sleep(5)
     driver.switch_to.window("window")

def login(driver,user_account,password_account):
    
    try:
       driver.find_element_by_xpath("//input[@id='login-username']").send_keys(user_account)
       driver.find_element_by_xpath("//input[@id='login-password']").send_keys(password_account)
       driver.find_element_by_xpath("//button[@id='login-button']").click()
       sleep(5)
    except NoSuchElementException:
       driver.close()

def default_ua(driver):
    driver.get("chrome-extension://lkmofgnohbedopheiphabfhfjgkhfcgf/popup.html")
    try:
       driver.find_element_by_xpath("//a[@id='default']").click()
       sleep(5)
    except NoSuchElementException:
       print("X 3")


def finish(proxy_ip,user_account,cnx,msg):
    try:          
         cursor = cnx.cursor()               
         cursor.execute("UPDATE `log` SET `next_start`='"+msg+"' WHERE `proxy` = '"+proxy_ip+"' and `account` = '" +user_account+ "' ")
         cnx.commit()  
    except MySQLdb.Error as err:  
         print("Something went wrong: (album) {}".format(err))  

def error_account(user_account,password_account,cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute("UPDATE `account` SET `error`=3 WHERE `user`='"+user_account+"' and `password`='"+str(password_account)+"'")
        cnx.commit() 
    except MySQLdb.Error as err:
        print("Something went wrong: (connection) {}".format(err))

def killed_account(user_account):
    try:  
        cnx = connectiondb()
        cursor = cnx.cursor()
        cmd="UPDATE `account` SET `error`=4 WHERE `user`='"+user_account+"' "
        print(cmd)
        cursor.execute(cmd)
        cnx.commit() 
    except MySQLdb.Error as err:
        print("Something went wrong: (connection) {}".format(err))

def error_proxy(in_use_proxy,id_proxy,cnx):
    try:
         curs = cnx.cursor()
         in_use = int(in_use_proxy) + 5
         curs.execute("UPDATE proxies SET in_use = " + str(in_use) + " WHERE id = "+ str(id_proxy) )
         cnx.commit() 
    except MySQLdb.Error as err:
         print("Something went wrong: (Proxies update) {}".format(err))
