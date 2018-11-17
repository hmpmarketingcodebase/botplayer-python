from requests import get
from time import sleep
import MySQLdb

#get public ip
try:
   mypubilcip = get('http://list.didsoft.com/get?email=zzakariaa10@yahoo.fr&pass=c3ui3z&pid=http2000').text
except:
   mypubilcip = "-"

proxies = mypubilcip.split('\n')

i = 0
while 1:

 for proxy in proxies:
  try:
    req =""
    #print(proxy)
    ip = proxy.split("#")[0]
    if ("#" in proxy):
       country = proxy.split("#")[1]
    if country.lower() in ('jp','fr','de','it','no','es','se','gb','ca','us','au','nz'):
      req = "{0}('{1}', '{2}', '-1', '0', '', ''),".format(req, ip,country)
      try:
        print(proxy)
        cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",'spoti')
        cmd = "INSERT INTO proxies2(proxie_port, country, in_use, error, user, password) VALUES {}".format(req)
        cmd = cmd[:-1]
        cursor = cnx.cursor()
        cursor.execute(cmd)
        cnx.commit() 
        i=i+1
        print("inserted : " + str(i) )
      except:
        err=1

    elif country.lower() in ('jp','il','ad','at','be','dk','fi','fr','de','gr','hu','is','ie','it','mt','mc','nl','no','pl','pt','ro','sk','es','se','ch','tr','gb','mx','ca','us','za','au','nz','dz','bh','eg','jo','kw','lb','ma','om','ps','qa','sa','tn','ae'):
      req = req + "('"+ip+"', '"+country+"', '0', '0', '', ''),"
      try:
        cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",'spoti')
        cmd = "INSERT INTO proxies2(proxie_port, country, in_use, error, user, password) VALUES {}".format(req)
        cmd = cmd[:-1]
        cursor = cnx.cursor()
        cursor.execute(cmd)
        cnx.commit() 
        i=i+1
        print("inserted : " + str(i) )
      except:
        err=1
  except:
    err=1
 sleep(3600)
 print("wait()")