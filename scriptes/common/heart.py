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
import platform
from urllib.parse import quote
import psutil
import random

def connectiondb(database):
   cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",database)    
   #cnx = MySQLdb.connect("10.128.0.2","spoti","o85BIgDEfChf","spoti")    
   return cnx
   
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

def proxy_in_use(in_use_proxy,id_proxy,cnx):
    try:
         curs = cnx.cursor()
         in_use = int(in_use_proxy) + 1
         curs.execute("UPDATE proxies SET in_use = " + str(in_use) + " WHERE id = "+ str(id_proxy) )
         cnx.commit() 
    except MySQLdb.Error as err:
         print("Something went wrong: (Proxies update) {}".format(err))

def proxy_connect(proxy,port,driver):
    driver.get("chrome-extension://fhnlhdgbgbodgeeabjnafmaobfomfopf/options.html?host="+proxy+"&port="+port)
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
    try:
        driver.find_element_by_xpath("//span[@id='http']").click()
    except NoSuchElementException:
        print("X 1")
    sleep(3)

def account(cnx):
      try:
         curs = cnx.cursor()
         curs.execute("select * from account where error = 2 order by in_use asc, RAND()")
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

def artist_id(cnx,id):
      try:
         curs = cnx.cursor()
         curs.execute("select * from artist where id  = " + str(id))
         artists = curs.fetchone()
         return artists
      except MySQLdb.Error as err:  
         print("Something went wrong: (artists) {}".format(err))   

def log_insert(proxy_ip,user_account,next_start,mypulicip,type_,cnx):
      print("# log insert")
      try:
         curs = cnx.cursor()
         curs.execute("INSERT INTO `log`(`proxy`, `account`, `next_start`, `number_play`, `ip`, `seconds`, `type`) VALUES ('"+proxy_ip+"','"+user_account+"','"+next_start+"',0,'"+ mypulicip +"',0,'"+type_+"')")
         cnx.commit() 
      except MySQLdb.Error as err:  
         print("Something went wrong: (by search) {}".format(err))  

def log_update(rep,proxy_ip,user_account,cnx,database):
      try:          
          print("#Log Update")
          cnx = connectiondb(database)
          cursor = cnx.cursor()               
          cursor.execute("UPDATE `log` SET `number_play`="+str(rep)+"  WHERE `proxy` = '"+proxy_ip+"' and `account` = '" +user_account+ "' ")
          cnx.commit()  
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

def config_driver():
 PROXY = "10.128.0.2:8080" # IP:PORT
 sleep(int(random.randrange(1,60))) 
 os= platform.system() #operation system (windows or linux)
 if (os=='Linux'):
  try:
    #print(path.dirname(path.abspath(__file__)))
    direct = (path.abspath(path.join(path.dirname( __file__ ), '../..', 'tools')))
    executable_path = direct + "/chromedriver"
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    #chrome_options.add_argument('--proxy-server=%s' % PROXY)
    chrome_options.add_extension(direct+'/Chrome-proxy-helper-master.crx')
    chrome_options.add_extension(direct+ '/extension_2_0_0_0.crx')
    chrome_options.add_extension(direct+'/Quick-Language-Switcher_v0.0.0.4.crx')
    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    #driver.maximize_window()
    driver.delete_all_cookies()
    clear_cache(driver)
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
    #chrome_options.add_argument('--proxy-server=%s' % PROXY)
    chrome_options.add_extension('../../tools/Chrome-proxy-helper-master.crx')
    chrome_options.add_extension('../../tools/extension_2_0_0_0.crx')
    chrome_options.add_extension('../../tools/Quick-Language-Switcher_v0.0.0.4.crx')
    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.delete_all_cookies()
    clear_cache(driver)
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

def random_ua(driver,database):
     try:  
        cnx = connectiondb(database)
        curs = cnx.cursor()
        curs.execute("select * from user_agent order by RAND()")
        ua = curs.fetchone() 
        cnx.commit() 
     except MySQLdb.Error as err:
        print("Something went wrong: (connection) {}".format(err))
     #Mobile user agent click extension
     sleep(5)
     driver.get("chrome-extension://lkmofgnohbedopheiphabfhfjgkhfcgf/popup.html")
     inpu_ua = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'ua'))) 
     inpu_ua.send_keys(ua[1])
     driver.execute_script("window.open('about:blank', 't2');")
     sleep(2)
     customButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'customButton'))) 
     customButton.click()
     sleep(2)
            
def error_proxy(in_use_proxy,id_proxy,cnx):
    try:
         curs = cnx.cursor()
         in_use = int(in_use_proxy) + 5
         curs.execute("UPDATE proxies SET in_use = " + str(in_use) + " WHERE id = "+ str(id_proxy) )
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
