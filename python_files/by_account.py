from heart import connectiondb
from account_checker2 import checker
import MySQLdb
from time import sleep
from pyvirtualdisplay import Display
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
display = Display(visible=0, size=(1366, 768))
from heart import proxis
display.start()
try: 

  try:
    cnx = connectiondb()
  except MySQLdb.Error as err:
    print("Error connection")
  proxy = proxis(country,cnx)
  proxy_ip = str(proxy[1])
  checker(str(proxy_ip.split(':')[0]),str(proxy_ip.split(':')[1]))

except:
      try:
         driver.close() 
      except :
         sleep(1)
         print("WebDriverException")
