import os
import sys
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
import platform
from urllib.parse import quote
import psutil
import random
import subprocess
import shutil
import json
import csv
#gggggggggg
def connectiondb(database):
   #cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",database)    
   #cnx = MySQLdb.connect("localhost","user",",Dc7aUb)3t>H@1.",database)    
   cnx = MySQLdb.connect("10.142.0.2","root","anoualwifi10",database)    
   return cnx
'''     
def proxis(country,cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from proxies where country='" + str(country) + "' order by in_use asc, RAND()")  
         proxy = curs.fetchone()
         if(proxy is None ):   
           curs .execute("select * from proxies order by in_use asc, RAND()")  
           proxy = curs.fetchone()
         return proxy
      except MySQLdb.Error as err:  
         print("Something went wrong: (proxies select) {}".format(err))     
'''

def proxis(cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from proxies order by in_use asc, RAND()")  
         proxy = curs.fetchone()
         return proxy
      except MySQLdb.Error as err:  
         print("Something went wrong: (proxies select) {}".format(err))     
		 
		 

def proxis2(cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from proxies2 where error =0 and in_use <4 order by in_use asc, RAND()")  
         proxy = curs.fetchone()
         return proxy
      except MySQLdb.Error as err:  
         print("Something went wrong: (proxies select) {}".format(err))     

def proxy_in_use(id_proxy,cnx):
    try:
         curs = cnx.cursor()
         curs.execute("UPDATE proxies SET in_use = in_use + 1 WHERE id = "+ str(id_proxy) )
         cnx.commit() 
    except MySQLdb.Error as err:
         print("Something went wrong: (Proxies update) {}".format(err))


def proxy_in_use2(id_proxy,cnx):
    try:
         curs = cnx.cursor()
         curs.execute("UPDATE proxies2 SET in_use = in_use + 1 WHERE id = "+ str(id_proxy) )
         cnx.commit() 
    except MySQLdb.Error as err:
         print("Something went wrong: (Proxies update) {}".format(err))
		 
def proxy_error2(proxy,cnx):
    try:
         print("gg")
         curs = cnx.cursor()
         print("UPDATE proxies2 SET error = -1 WHERE proxie_port = '"+ str(proxy)+"'")
         curs.execute("UPDATE proxies2 SET error = -1 WHERE proxie_port = '"+ str(proxy)+"'" )
         cnx.commit() 
    except MySQLdb.Error as err:
         print("Something went wrong: (Proxies update) {}".format(err))

def proxy_used(proxy,cnx,playlist,driver):
      try:
         curs = cnx.cursor()
         now = datetime.datetime.now()
         curs.execute("select * from log where realip='" + str(proxy) + "' and month(next_start)='"+str(now.month)+"' and day(next_start)='"+str(now.day)+"' and year(next_start) = '"+str(now.year)+"' and next_start<>'Error Proxy!' and next_start<>'finish' and playlist= '"+str(playlist)+"'")  
         proxy = curs.fetchone()
         
         if(proxy is None ):   
           return 1
         else:
           print("proxy used + " + str(proxy))
           driver.close()
   
      except MySQLdb.Error as err:  
         print("Something went wrong: (proxies select) {}".format(err))
   
      except MySQLdb.Error as err:  
         print("Something went wrong: (proxies select) {}".format(err))
		 
def proxy_used_id(proxy,cnx,driver,id,playlist,type):
      try:
         curs = cnx.cursor()
         now = datetime.datetime.now()
         r = "select * from log where realip='" + str(proxy) + "' and month(next_start)='"+str(now.month)+"' and day(next_start)='"+str(now.day)+"' and year(next_start) = '"+str(now.year)+"' and next_start<>'Error Proxy!' and id<>'"+str(id)+"' and playlist ='" + str(playlist) + "'"  
         print(r)
         curs.execute(r)  
         proxy = curs.fetchone()
         
         if(proxy is None ):   
           return 1
         else:
           if(type=='Album'):
              driver.close()
           print("Ip already exist id = " + str(id))
      except MySQLdb.Error as err:  
         print("Something went wrong: (proxies select) {}".format(err))

def proxy_connect(cnx,proxy,port,user,password,driver,mypublicip,type,playlist):
    try:
          driver.get("chrome-extension://fhnlhdgbgbodgeeabjnafmaobfomfopf/options.html?host="+proxy+"&port="+port+"&user="+user+"&pass="+password)
          driver.find_element_by_xpath("//input[@id='socks5']").click()
          sleep(2)
          driver.find_element_by_xpath("//input[@id='socks4']").click()
          sleep(2)
          driver.find_element_by_xpath("//input[@id='socks5']").click()
          sleep(2)
          driver.find_element_by_xpath("//input[@id='socks4']").click()
          sleep(2)
          driver.find_element_by_xpath("//input[@id='socks5']").click()
          sleep(3)
          driver.get("chrome-extension://fhnlhdgbgbodgeeabjnafmaobfomfopf/popup.html?host="+proxy+"&port="+port)
          sleep(3)    
       
          driver.find_element_by_xpath("//span[@id='http']").click()
    except NoSuchElementException:
        print("X 1")
        sleep(3)

    myip="--"
    mycountry="--"
    
    try:
        driver.get("http://www.geoplugin.net/json.gp")
        sleep(5)
        json_out = driver.find_element_by_xpath("//pre").text
        d = json.loads(json_out)
        mycountry = (d['geoplugin_countryCode'])
        myip = (d['geoplugin_request'])        
    except:
        try:
           driver.get("https://iplocation.com/")
           sleep(5)
           myip = driver.find_element_by_xpath("//table//td//b[@class='ip']").text
           mycountry = driver.find_element_by_xpath("//table//td//span[@class='country_name']").text
           dic = {}
           with open("../common/wikipedia-iso-country-codes.csv") as f: 
               reader = csv.DictReader(f, delimiter = ',')
               for row in reader:
                  if(row['name'] == mycountry):
                     mycountry = row['Alpha-2'].lower()
        except:
           myip = "--"
           mycountry="--"
    print(mycountry)
    #print(myip)
    if(type=='Album'):
        a = proxy_used(myip,cnx,playlist,driver)
    elif(type=='Artist'):
        a = 1
    print(myip  + " vs " + mypublicip) 
    if((a == 1) and  (myip != '--')):
       return myip + ";" + mycountry
    else: 
       if(myip == '--'):
          print("Error Proxy!!")
          proxy_ip = proxy + ":" + port
          current=datetime.datetime.now()
          log_insert(str(proxy_ip),str(myip),"Error proxy",str(current),mypublicip,"Error proxy","","",cnx)
          
       else:
          print("Ip already exist")
       return "error proxy"
       

def check_ip(ip,driver):
    myip = '--'
    try:
           #driver.get("http://www.geoplugin.net/json.gp")
           driver.execute_script("window.open('http://www.geoplugin.net/json.gp', 't3')")
           sleep(2)
           driver.switch_to.window("t3")
           sleep(2)
           json_out = driver.find_element_by_xpath("//pre").text
           d = json.loads(json_out)
           myip = (d['geoplugin_request'])    
           driver.close()   
           driver.switch_to.window("t2")
    except:
         try:
           #driver.get("https://iplocation.com/")
           driver.execute_script("window.open('https://iplocation.com/', 't3')")
           sleep(2)
           driver.switch_to.window("t3")
           sleep(2)
           myip = driver.find_element_by_xpath("//table//td//b[@class='ip']").text
           driver.close()
           driver.switch_to.window("t2")
         except :
           err=1
           driver.close()

    print(ip + " --- " + myip)
    if((ip != myip)and(myip != '--')):
        driver.close()              
    

  
def account(cnx,country,playlist_account):
      try:
         now = datetime.datetime.now()
         curs = cnx.cursor()
         curs.execute("select * from account where country = '" + country + "' and in_use =(select min(in_use) from account  where error = 2) and error = 2 order by  RAND()")
         #curs.execute("select * from account where country = '" + country + "' and error = 2 order by in_use asc,  RAND()")
         account = curs.fetchone() 
         #print("select * from account where country = '" + country + "' and in_use =(select min(in_use) from account  where error = 2) and error = 2 order by  RAND()")
         if(account is None ):   
           curs .execute("select * from account where in_use =(select min(in_use) from account  where error = 2)and error = 2 order by  RAND()")  
           #curs.execute("select * from account where error = 2 order by in_use asc,  RAND()")
           account = curs.fetchone()
         print("/////////////////")
         print(account)

         user = account[1]
         print("user = " + user)
         id_account = account[0]
         curs2 = cnx.cursor()
         req = "select * from log where account='" + str(user) + "' and month(next_start)='"+str(now.month)+"' and day(next_start)='"+str(now.day)+"' and year(next_start) = '"+str(now.year)+"' and next_start<>'Error Proxy!' and next_start<>'finish' and playlist_account='"+str(playlist_account)+"'"
         #print(req)
         curs2.execute(req)  
         acc = curs2.fetchone()
         account_in_use(id_account,cnx)
         
         if(acc is None ):   
           return account
         else:
           print("account used + " + str(acc))
           driver.close()
         
      except MySQLdb.Error as err:  
         print("Something went wrong: (Accounts) {}".format(err))   


def account2(cnx,country):
      try:
         now = datetime.datetime.now()
         curs = cnx.cursor()
         curs.execute("select * from account where error = 2 order by in_use asc,  RAND()")
         account = curs.fetchone() 
         return account
      except MySQLdb.Error as err:  
         print("Something went wrong: (Accounts) {}".format(err))   



def account_in_use(id_account,cnx):
      try:
         print("Update account")
         curs = cnx.cursor()
         curs.execute("UPDATE account SET in_use = in_use+1 WHERE id = "+ str(id_account) )
         cnx.commit() 
      except MySQLdb.Error as err:
         print("Something went wrong: {}".format(err))

		 
def client_play(play,client,cnx):
      try:
         print(" + " + str(play) + " to client n°" + str(client)) 
         curs = cnx.cursor()
         curs.execute("UPDATE `client` SET plays=plays+"+str(play)+" where id = " + str(client))
         cnx.commit() 
      except MySQLdb.Error as err:
         print("Something went wrong: {}".format(err))

def client_follow(client,cnx):
      try:
         print(" + 1 follow to client n°" + str(client)) 
         curs = cnx.cursor()
         curs.execute("UPDATE `client` SET follow=follow+1 where id = " + str(client))
         cnx.commit() 
      except MySQLdb.Error as err:
         print("Something went wrong: {}".format(err))

def songs(id_playlist,cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from songs where playlist >= " + str(id_playlist) + " order by RAND()")
         songs = curs.fetchall()
         #s = len(songs)
         #s = int(random.randint(int(int(s)/2),int(s)))
 
         #curs2 = cnx.cursor()
         #curs2.execute("select * from songs where playlist >= " + str(id_playlist) + " order by RAND() LIMIT " + str(s))
         #songs = curs2.fetchall()
         return songs
      except MySQLdb.Error as err:  
         print("Something went wrong: (song) {}".format(err)) 


def songs_album(id_album,playlist,cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from songs where album = '" + str(id_album) + "' and playlist = '" + str(playlist) + "' order by RAND()")
         songs = curs.fetchall()
         #s = len(songs)
         #s = int(random.randint(5,int(s)))

         #curs2 = cnx.cursor()
         #curs2.execute("select * from songs where album = '" + str(id_album) + "' order by RAND() LIMIT " + str(s))
         #songs = curs2.fetchall()
         
         return songs
      except MySQLdb.Error as err:  
         print("Something went wrong: (song) {}".format(err)) 


def songs_artist(id_artist,cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from songs where artist = '" + str(id_artist) + "' order by RAND()")
         songs = curs.fetchall()
         s = len(songs)
         s = int(random.randint(1,int(s)))

         curs2 = cnx.cursor()
         curs2.execute("select * from songs where artist = '" + str(id_artist) + "' order by RAND() LIMIT " + str(s))
         songs = curs2.fetchall()
         
         return songs
      except MySQLdb.Error as err:  
         print("Something went wrong: (song) {}".format(err)) 


def playlist_album(play_album,playlist,cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from playlist_album where play >= " + str(int(play_album)) + " and playlist = " + str(int(playlist)) + " order by RAND()")
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
         curs.execute("select * from artist where url<>'' and follow<>'0' order by RAND()")
         artists = curs.fetchall()
         return artists
      except MySQLdb.Error as err:  
         print("Something went wrong: (artists) {}".format(err))  

def follow_artist(cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from artist where url<>'' order by RAND()")
         artists = curs.fetchone()
         return artists
      except MySQLdb.Error as err:  
         print("Something went wrong: (artists) {}".format(err))   

def artist_id(cnx,id):
      try:
         curs = cnx.cursor()
         curs.execute("select * from artist where id  = " + str(id))
         artists = curs.fetchone()
         return artists
      except MySQLdb.Error as err:  
         print("Something went wrong: (artists) {}".format(err))   

def log_insert(proxy_ip,myip,user_account,next_start,mypulicip,type_,playlist,playlist_account,cnx):
      print("# log insert")
      try:
         curs = cnx.cursor()
         req = "INSERT INTO `log`(`proxy`, `account`, `next_start`, `number_play`, `ip`, `seconds`, `type`, `realip`, `playlist`, `playlist_account`) VALUES ('"+proxy_ip+"','"+user_account+"','"+next_start+"',0,'"+ mypulicip +"',0,'"+type_+"','"+myip+"','"+str(playlist)+"','"+str(playlist_account)+"')"
         print(req)
         curs.execute(req)
         cnx.commit() 
      except MySQLdb.Error as err:  
         print("Something went wrong: (by search) {}".format(err))  
      return (str(curs.lastrowid))
  
def log_update(id,tot,database):
      try:          
        if(int(tot)>0):
          print("#Log Update")
          cnx = connectiondb(database)
          cursor = cnx.cursor()               
          #cursor.execute("UPDATE `log` SET `number_play`="+str(rep)+"  WHERE `proxy` = '"+proxy_ip+"' and `account` = '" +user_account+ "' ")
          cursor.execute("UPDATE `log` SET `number_play`="+str(tot)+" WHERE id = "+str(id))
          cnx.commit()
          print("UPDATE `log` SET `number_play`="+str(tot)+" WHERE id = "+str(id))
          print("# Updated")
      except MySQLdb.Error as err:  
          print("Something went wrong: (search) {}".format(err))   

def select_account_geo(cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from account where country ='0' and error <> '1' order by RAND()")
         account = curs.fetchone() 
         return account
      except MySQLdb.Error as err:  
         print("Something went wrong: (Accounts) {}".format(err))  

def select_account_(cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from account where error = 0 order by RAND()")
         account = curs.fetchone() 
         return account
      except MySQLdb.Error as err:  
         print("Something went wrong: (Accounts) {}".format(err))   


#account_geo 
def account_geo(cnx,count,location,user,password,database):
      try:          
          cnx = connectiondb(database)
          cursor = cnx.cursor()               
          cursor.execute("UPDATE `account` SET `country`='"+str(count).lower()+"', `location`='"+str(location).lower()+"' where user = '" +user+ "' and password ='" +password+ " '")
          cnx.commit()  
      except MySQLdb.Error as err:  
          print("Something went wrong: (search) {}".format(err))   
 

def next_run(next_start,proxy_ip,user_account,database):
         try:          
            cnx = connectiondb(database)
            curs = cnx.cursor()               
            curs.execute("UPDATE `log` SET `next_start`='"+str(next_start)+"' WHERE `proxy` = '"+proxy_ip+"' and `account` = '" +user_account+ "' ")
            cnx.commit()  
         except MySQLdb.Error as err:  
            print("Something went wrong: (search) {}".format(err))   


def get_clear_browsing_button(driver):
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    driver.get('chrome://settings/clearBrowserData')
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)
    get_clear_browsing_button(driver).click()
    wait.until_not(get_clear_browsing_button)
    sleep(5)

def config_driver(database,device,prox):
 #PROXY = "107.178.4.215:35892" # IP:PORT
 #PROXY = "107.178.4.215:35892" # IP:PORT
 PROXY = prox # IP:PORT
 sleep(int(random.randint(1,10))) 
 try:  
        cnx = connectiondb(database)
        curs = cnx.cursor()
        curs.execute("select * from user_agent where device = '"+device+"' order by RAND()")
        ua = curs.fetchone() 
        cnx.commit() 
 except MySQLdb.Error as err:
        print("Something went wrong: (connection) {}".format(err))

 os= platform.system() #operation system (windows or linux)
 if (os=='Linux'):
  try:
    #print(path.dirname(path.abspath(__file__)))
    direct = (path.abspath(path.join(path.dirname( __file__ ), '../..', 'tools')))
    executable_path = direct + "/chromedriver"
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--disable-setuid-sandbox")

    #chrome_options.add_argument('--proxy-server=%s' % PROXY)
    chrome_options.add_extension(direct+'/Chrome-proxy-helper-master.crx')
    chrome_options.add_extension(direct+ '/extension_2_0_0_0.crx')
    chrome_options.add_extension(direct+'/Quick-Language-Switcher_v0.0.0.4.crx')
    chrome_options.add_extension(direct+'/ua.crx')
    print(ua[1])
    chrome_options.add_argument("user-agent=" + ua[1])
    if(device=='mobile'):
       devices = ['Nexus 5','Blackberry PlayBook','Pixel 2','Nexus 6P','iPhone 8 Plus','iPhone 7 Plus','Nokia N9','Nokia Lumia 520','Galaxy S5','iPhone 7','LG Optimus L70','iPhone 5','iPhone 4','Nexus 10','iPhone 8','iPhone 6','Galaxy S III','iPhone 7','iPhone SE','Microsoft Lumia 550','iPad Mini','iPhone 5/SE','iPad Pro','Nexus 5X','iPhone 6 Plus','iPhone 7 Plus','iPhone 8 Plus','Galaxy Note II','iPhone X','Microsoft Lumia 950','Pixel 2 XL','Galaxy Note 3','Kindle Fire HDX','iPad','BlackBerry Z30','Nexus 6','Nexus 7','Nexus 4']
       random.shuffle(devices)
       mobile_emulation = { "deviceName": devices[1] }
       chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    #chrome_options = webdriver.ChromeOptions()
    if(prox!="x"):
       chrome_options.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    driver.delete_all_cookies()
    clear_cache(driver)
    #driver.maximize_window()
    return driver  
  except ConnectionResetError:
    sleep(1)
    print("linux error")
 elif (os=='Windows'):
  try:
    
    executable_path = "../../tools/chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--enzzdzable-extensions")
    #chrome_options.add_argument('--proxy-server=%s' % PROXY)
    chrome_options.add_extension('../../tools/Chrome-proxy-helper-master.crx')
    chrome_options.add_extension('../../tools/extension_2_0_0_0.crx')
    chrome_options.add_extension('../../tools/ua.crx')
    chrome_options.add_extension('../../tools/Quick-Language-Switcher_v0.0.0.4.crx')
    chrome_options.add_argument("user-agent=" + ua[1])
     
    if(device=='mobile'):
       devices = ['Nexus 5','Blackberry PlayBook','Pixel 2','Nexus 6P','iPhone 8 Plus','iPhone 7 Plus','Nokia N9','Nokia Lumia 520','Galaxy S5','iPhone 7','LG Optimus L70','iPhone 5','iPhone 4','Nexus 10','iPhone 8','iPhone 6','Galaxy S III','iPhone 7','iPhone SE','Microsoft Lumia 550','iPad Mini','iPhone 5/SE','iPad Pro','Nexus 5X','iPhone 6 Plus','iPhone 7 Plus','iPhone 8 Plus','Galaxy Note II','iPhone X','Microsoft Lumia 950','Pixel 2 XL','Galaxy Note 3','Kindle Fire HDX','iPad','BlackBerry Z30','Nexus 6','Nexus 7','Nexus 4']
       random.shuffle(devices)
       mobile_emulation = { "deviceName": devices[1] }
       chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    if(prox!="x"):
       #chrome_options = webdriver.ChromeOptions()
       chrome_options.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    driver.delete_all_cookies()
    clear_cache(driver)
    driver.maximize_window()
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

def language_browser(lang,driver):
     print ("language is " + lang)  
     if(lang=='all'):
          lang = 'en'
     #Mobile user agent click extension
     
     if(lang != 'en' and lang != 'de' and lang != 'pl' and lang != 'zh' and lang != 'all'):
        driver.get("chrome-extension://pmjbhfmaphnpbehdanbjphdcniaelfie/options.html")
        i=0
        p=0
        while(i<34):
              i=i+1
              try:
                 a = driver.find_element_by_xpath("//table[@class='table']//tbody[@id='locales-builtIn']//tr["+str(i)+"]//td[3]//span")
                 if(a.text == lang):
                    p=i
                    i=34
              except:
                 b=''
        if(p==0):
           p=2
           lang='en'
        driver.find_element_by_xpath("//table[@class='table']//tbody[@id='locales-builtIn']//tr["+str(p)+"]//td[1]//input").click()
        sleep(5)        
        driver.get("chrome-extension://pmjbhfmaphnpbehdanbjphdcniaelfie/popup.html")
        try:
           driver.find_element_by_xpath("//li[@data-value='"+lang+"']").click()
           sleep(5)
        except NoSuchElementException:
           print("NoSuchElementException : language user")
            
     else:
       driver.get("chrome-extension://pmjbhfmaphnpbehdanbjphdcniaelfie/popup.html")
       try:
           driver.find_element_by_xpath("//li[@data-value='"+lang+"']").click()
       except NoSuchElementException:
           print("NoSuchElementException : language user") 
    #end Mobile user agent click extension
     sleep(5)

def login(driver,user_account,password_account):
    
    try:
       driver.find_element_by_xpath("//input[@id='login-username']").clear()
       sleep(1)
       driver.find_element_by_xpath("//input[@id='login-password']").clear()
       sleep(2)
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
    driver.execute_script("window.open('about:blank', 't2');")
    driver.close()


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
        cursor.execute("UPDATE `account` SET `error`=1 WHERE `user`='"+user_account+"' and `password`='"+str(password_account)+"'")
        cnx.commit() 
    except MySQLdb.Error as err:
        print("Something went wrong: (connection) {}".format(err))

def valid_account(user_account,password_account,cnx):
    try:
        cursor = cnx.cursor()
        cursor.execute("UPDATE `account` SET `error`=2 WHERE `user`='"+user_account+"' and `password`='"+str(password_account)+"'")
        cnx.commit() 
    except MySQLdb.Error as err:
        print("Something went wrong: (connection) {}".format(err))

def killed_account(user_account,database):
    try:  
        cnx = connectiondb(database)
        cursor = cnx.cursor()
        cmd="UPDATE `account` SET `error`=4 WHERE `user`='"+user_account+"' "
        print(cmd)
        cursor.execute(cmd)
        cnx.commit() 
    except MySQLdb.Error as err:
        print("Something went wrong: (connection) {}".format(err))

def random_ua(driver,database,device):
     try:  
        cnx = connectiondb(database)
        curs = cnx.cursor()
        curs.execute("select * from user_agent where device = '"+device+"' order by RAND()")
        ua = curs.fetchone() 
        cnx.commit() 
     except MySQLdb.Error as err:
        print("Something went wrong: (connection) {}".format(err))
     #Mobile user agent click extension
     sleep(5)
     driver.get("chrome-extension://djflhoibgkdhkhhcedjiklpkjnoahfmg/options.html")
     add_ua_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'add_ua_name'))) 
     add_ua_user_agent = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'add_ua_user_agent'))) 
     add_ua_group = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'add_ua_group'))) 
     add_ua_indicator = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'add_ua_indicator'))) 
     add_ua_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'add_ua_button'))) 
     add_ua_name.send_keys("xx")
     add_ua_user_agent.send_keys(ua[1])
     sleep(1)
     add_ua_group.clear()
     sleep(2)
     add_ua_group.send_keys("xx")
     add_ua_indicator.send_keys("xx")
     sleep(2)
     add_ua_button.click()
     sleep(1)
     driver.get("chrome-extension://djflhoibgkdhkhhcedjiklpkjnoahfmg/popup.html")
     xx = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'ua_row_5'))) 
     xx.click() 
     sleep(2) 
     xx = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'ua_row_c_15'))) 
     xx.click() 
     sleep(5)    
     driver.execute_script("window.open('about:blank', 't2');")
     driver.close()

'''
     inpu_ua = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'ua'))) 
     inpu_ua.send_keys(ua[1])
     driver.execute_script("window.open('about:blank', 't2');")
     sleep(2)
     customButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'customButton'))) 
     #customButton.click()
     sleep(2)
     #driver.close()      
'''


def error_proxy(id_proxy,cnx):
    try:
         curs = cnx.cursor()
         print("UPDATE proxies2 SET error = 1 WHERE id = "+ str(id_proxy) )
         curs.execute("UPDATE proxies2 SET error = 1 WHERE id = "+ str(id_proxy) )
         cnx.commit() 
    except MySQLdb.Error as err:
         print("Something went wrong: (Proxies update) {}".format(err))



def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

	
  
def clean_memory():
  # cmd=('sudo bash clean_ram.sh & disown')
  # subprocess.call(cmd, shell=True, cwd='../common/')
  # sleep(5)
  # cmd=('sudo bash clean_tmp.sh & disown')
  # subprocess.call(cmd, shell=True, cwd='../common/')

  # sleep(5)
   mem = psutil.virtual_memory()
   mem_ = sizeof_fmt(mem.free)
   print('Free memory :'+ str(mem_))
   if('MiB' in mem_):
      s = mem_[:-3]
      #print('memory use:'+ str(s))
      if(float(s) < 100 ):
         print("process killed")         
         os.system("killall chrome chromedriver")
         sleep(5)
         
def kill_process(parent_pid):
   os.system("pkill -TERM -P " + str(parent_pid))
   print("# " + str(parent_pid) + " Killed")


def read_log_update(id,database,pat):
   print("#####ssss#######")
   try:
     # file = open("../spotify/log/"+str(id), "r")
      file = open(pat+str(id), "r")

      tot = file.read()
      print("#####Tot#######")
      try:
        print("##Log Update##")
        cnx = connectiondb(database)
        cursor = cnx.cursor()
        
        cursor.execute("UPDATE `log` SET `number_play`="+str(tot)+" WHERE id = "+str(id))
        cnx.commit()
        ff= str(id)

        cmd=('sudo rm '+str(ff))
        if(database == "spoti"):
           subprocess.call(cmd, shell=True, cwd='../spotify/log/')
        elif(database == "deezer"):
           subprocess.call(cmd, shell=True, cwd='../deezer/log/')

      except MySQLdb.Error as err:
          print("Something went wrong: (search) {}".format(err))
   except:
      err = 1