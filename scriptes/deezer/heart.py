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
from selenium.common.exceptions import TimeoutException
import random
import sys
from urllib.parse import quote
sys.path.append("..")
import common.heart

#check if proxy is ok
def check_proxy(driver):
    try:
      WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login_mail')))
      print (" > Proxy is ready!")
      connect_proxy=1
    except TimeoutException:
      try:
         driver.get("https://www.deezer.com/login")
         WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login_mail')))
         print (user_account + " > Proxy is ready!")
         connect_proxy=1
      except TimeoutException:
         try:
            driver.get("https://www.deezer.com/login")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login_mail')))
            print (user_account + " > Proxy is ready!")
            connect_proxy=1
         except TimeoutException:
            driver.get("https://www.deezer.com/login")
            print (user_account + " > Loading took too much time! (proxy)")
            connect_proxy=0 
            try:
                driver.close() 
            except:
                sleep(1)
    return  connect_proxy
   
def login(driver,user_account,password_account):
    try:
          driver.execute_script("window.scrollBy(0, 500);")
          WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login_mail'))).send_keys(user_account)
          WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login_password'))).send_keys(password_account)
          WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login_form_submit'))).click()
          print (user_account + " > Proxy is ready!")
          connect_proxy=1
    except :
          driver.refresh()
          WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login_mail'))).send_keys(user_account)
          WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login_password'))).send_keys(password_account)
          WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'login_form_submit'))).click()
          print (user_account + " > Proxy is ready!")
          connect_proxy=1

def left_search(driver,song_name,song_artist_name):
    srch = song_name + " " + song_artist_name
    try:
      try:
         wait = WebDriverWait(driver, 30)
         disonnect(driver)
         a =  wait.until(EC.element_to_be_clickable((By.ID,  "menu_search")))
         a.click()
      except :
         driver.refresh()
         disonnect(driver)
         a =  wait.until(EC.element_to_be_clickable((By.ID, "menu_search")))
         a.click()
    except :
      driver.refresh()
      disonnect(driver)
      a =  wait.until(EC.element_to_be_clickable((By.ID, "menu_search")))
      a.click()
    disonnect(driver)
    search = wait.until(EC.element_to_be_clickable((By.ID, "menu_search")))
    search.clear()
    sleep(3)
    search.clear()
    search.send_keys(srch)
    sleep(5)
    try:
           sleep(5)
           disonnect(driver)
           wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='panel-search-suggest']"))).click()
           wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']")))
    except:
           try:
               disonnect(driver)
               search = wait.until(EC.element_to_be_clickable((By.ID, "menu_search")))
               search.clear()
               sleep(3)
               disonnect(driver)
               search.clear()
               search.send_keys(srch)
               sleep(5)
               disonnect(driver)
               wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='panel-search-suggest']"))).click()
               wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']")))
           except:
               try:
                  driver.refresh()
                  disonnect(driver)
                  search =  wait.until(EC.element_to_be_clickable((By.ID, "menu_search")))
                  search.click()
                  sleep(5)
                  disonnect(driver)
                  search.send_keys(srch)
                  sleep(5)
                  wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='panel-search-suggest']"))).click()
                  wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']")))
               except:
                  try:
                   driver.refresh()
                   disonnect(driver)
                   search =  wait.until(EC.element_to_be_clickable((By.ID, "menu_search")))
                   search.click()
                   sleep(5)
                   disonnect(driver)
                   search.send_keys(srch)
                   sleep(5)
                   disonnect(driver)
                   wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='panel-search-suggest']"))).click()
                   wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']")))
                  except :
                   srch = quote(srch)
                   driver.get('https://www.deezer.com/search/'+srch)
                   try:
                      disonnect(driver)
                      a = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div[2][@itemprop='track']")))
                   except:
                      try:
                          disonnect(driver)
                          driver.get('https://www.deezer.com/search/'+srch)
                          a = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div[2][@itemprop='track']")))
                      except:
                          disonnect(driver)
                          driver.get('https://www.deezer.com/search/'+srch)
                          a = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div[2][@itemprop='track']")))
    sleep(5)

def right_search_and_play(driver,song_,artists,albums,type,pp,proxy_ip,user_account,next_start,mypubilcip,cnx):
 play=0 
 insert=0
 ii=0
 pl1=-1
 wait = WebDriverWait(driver, 30)
 for s in song_: 
    ii = ii +1
    song_name = s[1]
    song_duration = int(s[3])
    song_artist = int(s[6])
    song_artist_name = ""
    for a in artists:
         if(int(a[0]) == song_artist):
             song_artist_name = a[1]

    song_album = int(s[4])
    song_album_url = ""
    #get album name of the current song
    for al in albums:
         if(int(al[0]) == song_album):
            song_album_name = al[1]   
    disonnect(driver)
    sr = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='naboo_datagrid_filter_text']")))
    sr.click()
    sr.clear()
    sleep(3)
    sr.clear()
    sleep(3)
    sr.send_keys(song_name)
    sleep(3)
    sr.clear()
    sleep(3)
    sr.send_keys(song_name)
    sleep(3)
    disonnect(driver)
    a = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div[2][@itemprop='track']")))
    xx=0
    nn=0
    while((xx<50)and(nn<=0)):
           try:
              song_name_ = driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-title']").text
              artist_name_ = driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-artist']").text
              album_name_ =  driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-album']").text
              print("song name ^ " + song_name_ + " = " + song_name + " | " )
              print("artist name ^ " + artist_name_ + " = " + song_artist_name + " | " )
              print("album name ^ " + album_name_ + " = " + song_album_name + " | " )
              if ((song_name_ == song_name) and (song_artist_name in artist_name_) and (song_album_name == album_name_)):
                   print("+ " + song_name_ + "+ " + artist_name_ + " + " + album_name_)
                   try:
                      row =  driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']")
                      ActionChains(driver).double_click(row).perform()
                      nn=1
                   except:
                      err=1
                   
                   nn=1
           except:
              err=1
           xx=xx+1
    if(pp%10==0):
            ms=(random.randrange(int(song_duration) - int(margin_play) , int(song_duration)))
    else:
            ms=(random.randrange(40, 80))
    print(" > Playing : " + song_name + " in " + str(ms) + " seconds")
    i=0
    o = ms / 5
    while(i<o):
       sleep(5)
       try:
            driver.find_element_by_xpath("//div[@id='modal_limitation']//button[@class='btn btn-primary']").click()
            print("disconnect all other devices")
       except:
            try:
                driver.find_element_by_xpath("//div[@id='page_sidebar']//button[@class='control control-play']//span[@class='icon icon-play']")
                driver.find_element_by_xpath("//div[@id='page_sidebar']//button[@class='control control-play']").click()
                i=i+1
                print("palying >")
            except:
                print("playing >>")
                i=i+1
    print("yeaaah!!")
    play=play+1
    if(play == 3):
         pl1=1
    sleep(2)
    if(insert==0):
         common.heart.log_insert(proxy_ip,user_account,str(next_start),mypubilcip,type,cnx)
         insert=1
    else:
         common.heart.log_update(ii,proxy_ip,user_account,cnx,'deezer')
                             
 return pl1

def add_to_playlist(driver,song_name,song_artist_name,song_album_name):
    xx=1
    nn=0
    wait = WebDriverWait(driver, 30)
    while((xx<50)and(nn<=0)):
           try:
              song_name_ = driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-title']").text
              artist_name_ = driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-artist']").text
              album_name_ =  driver.find_element_by_xpath("//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell cell-album']").text
              print("song name ^ " + song_name_ + " = " + song_name + " | " )
              print("album name ^ " + album_name_ + " = " + song_album_name + " | " )
              print("artist name ^ " + artist_name_ + " = " + song_artist_name + " | " )
              if ((song_name_ == song_name) and (song_artist_name in artist_name_) and (song_album_name == album_name_)):
                   print("+ " + song_name_ + "+ " + artist_name_ + " + " + album_name_)
                   try:
                      l =  wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']")))
                      ActionChains(driver).move_to_element(l).perform() 
                      wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='datagrid']//div["+str(xx)+"][@itemprop='track']//div[@class='datagrid-cell datagrid-cell-hover datagrid-cell-action']//button[@class='action-item-btn datagrid-action']"))).click()
                      print("Add to playlist click")
                      sleep(5)
                      wait.until( EC.presence_of_element_located((By.XPATH, "//div[@class='popover popover-left')]//div[@class='playlist-container nano has-scrollbar')]")))
                      print(song_name_ + " to " + playlist_name)
                      sleep(5) 
                   except:
                      err=1    
                   nn=1
           except:
              err=1
           xx=xx+1
		   
def search_playlist(driver,playlist_name):
    continue_=0
    wait = WebDriverWait(driver, 30)
    #find playlist name in playlist list
    try:
       
       wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-type='playlists']"))).click()
       wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='panel-playlists']//a[@class='link-animated']"))).click()
       srch_pl = wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='user-section']//div[@class='action-top-page']//div[@class='btn-group user-search']//input[@class='form-control']")))
       srch_pl.click()
       srch_pl.clear()
       sleep(3)
       srch_pl.clear()
       sleep(3)
       srch_pl.send_keys(playlist_name)
       sleep(3)
       srch_pl.clear()
       srch_pl.send_keys(playlist_name)
       wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='container']")))
       driver.find_element_by_link_text(playlist_name).click()
       continue_=1
    except:
       try:
           driver.refresh()
           if("playlists" not in driver.current_url):
              wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-type='playlists']"))).click()
              wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='panel-playlists']//a[@class='link-animated']"))).click()  
           srch_pl = wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='user-section']//div[@class='action-top-page']//div[@class='btn-group user-search']//input[@class='form-control']")))
           srch_pl.click()
           srch_pl.clear()
           sleep(3)
           srch_pl.clear()
           sleep(3)
           srch_pl.send_keys(playlist_name)
           sleep(3)
           srch_pl.clear()
           srch_pl.send_keys(playlist_name)
           wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='container']")))
           driver.find_element_by_link_text(playlist_name).click()
           continue_=1
       except:
          try:
           driver.refresh()
           if("playlists" not in driver.current_url):
              wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-type='playlists']"))).click()
              wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='panel-playlists']//a[@class='link-animated']"))).click()  
           srch_pl = wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='user-section']//div[@class='action-top-page']//div[@class='btn-group user-search']//input[@class='form-control']")))
           sleep(5)
           srch_pl.click()
           srch_pl.clear()
           sleep(3)
           srch_pl.clear()
           sleep(3)
           srch_pl.send_keys(playlist_name)
           sleep(3)
           srch_pl.clear()
           srch_pl.send_keys(playlist_name)
           wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='container']")))
           driver.find_element_by_link_text(playlist_name).click()
           continue_=1
          except:
           continue_=0
    return continue_

def disonnect(driver):
    try:
       driver.find_element_by_xpath("//div[@id='modal_limitation']//button[@class='btn btn-primary']").click()
       print("disconnect all other devices")
    except:
       err=1