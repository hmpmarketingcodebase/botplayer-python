from requests import get
from time import sleep
import MySQLdb

i = 0
while 1:
#get public ip
 try:
   mypubilcip = get('http://list.didsoft.com/get?email=zzakariaa10@yahoo.fr&pass=c3ui3z&pid=http2000&https=yes').text
 except:
   mypubilcip = "-"
 proxies = mypubilcip.split('\n')
 min = 0
 '''
 try:
    cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",'spoti')
    curs = cnx.cursor()
    curs.execute("select min(in_use) as min from proxies2 where error =0")  
    min = curs.fetchone()[0]
 except MySQLdb.Error as err:  
    print("Something went wrong: (proxies select) {}".format(err))    
 if (min == None):
     min=0
 print("min is " + str(min) )
 '''
 for proxy in proxies:
  try:
    req =""
    #print(proxy)
    ip = proxy.split("#")[0]
    if ("#" in proxy):
       country = proxy.split("#")[1]
    if country.lower() in ('jp','fr','de','it','no','es','se','gb','ca','us','au','nz','nl','bg'):
      req = "{0}('{1}', '{2}', '{3}', '0', '', ''),".format(req, ip,country,min)
      try:
        
        cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",'spoti')
        cmd = "INSERT INTO proxies2(proxie_port, country, in_use, error, user, password) VALUES {}".format(req)
        cmd = cmd[:-1]
        cursor = cnx.cursor()
        cursor.execute(cmd)
        cnx.commit() 
        i=i+1
        print("inserted : " + str(proxy) )
      except:
        err=1

    elif country.lower() in ('jp','il','ad','at','be','dk','fi','fr','de','gr','hu','is','ie','it','mt','mc','nl','no','pl','pt','ro','sk','es','se','ch','tr','gb','mx','ca','us','za','au','nz','dz','bh','eg','jo','kw','lb','ma','om','ps','qa','sa','tn','ae'):
      req = req + "('"+ip+"', '"+country+"', '"+min+"', '0', '', ''),"
      try:
        cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",'spoti')
        cmd = "INSERT INTO proxies2(proxie_port, country, in_use, error, user, password) VALUES {}".format(req)
        cmd = cmd[:-1]
        cursor = cnx.cursor()
        cursor.execute(cmd)
        cnx.commit() 
        i=i+1
        print("inserted : " + str(proxy) )
      except:
        err=1
  except:
    err=1
	
  '''
  try:
        cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",'spoti')
        cmd2 = "delete from proxies2 where in_use > 2 or error = -1"
        cursor = cnx.cursor()
        cursor.execute(cmd2)
        cnx.commit()
        print("deleted : ")
  except:
        err=1
  '''
 print("wait()")
 sleep(1000)
 