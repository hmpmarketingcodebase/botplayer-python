from requests import get
from time import sleep
import MySQLdb
from urllib.request import Request, urlopen
import requests
#get public ip


i = 0

while 1:
 i=0
 ii=0
 try:
   mypubilcip = get('http://pubproxy.com/api/proxy?limit=20&format=txt').text
 except:
   mypubilcip = "-"

 
 prox = mypubilcip.split('\n')
 for ip in prox:
    try:
      aa = ip
      ii+=1
      i=i+1
      url = 'http://www.proxy-checker.org/result.php?list='+ip
      req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
      webpage = urlopen(req).read()
      codes = str(webpage).split(' code=')
      code = codes[1]
      code = code[2:8]
      
   
      json_data = {"proxy": ip, "code": code}
      req = requests.post("http://www.proxy-checker.org/checkproxy.php", data={"proxy": ip, "code": code})
      
      a = str(req.text)
      count = str(a).split("alt")
      country = count[1]
      country = country[3:5]
      ips = str(a).split(" /></td><td>")
      ip = ips[1].split("__")
      myip = ip[0].replace('</td><td>',"#")
      myip = myip.replace('</td>',"")
      myip1 = aa+"#"+country
      req = ""
      if("working" in str(myip)):
      
         ip = myip1.split("#")[0]
         if ("#" in myip1):
            country = myip1.split("#")[1]
      
         if country.lower() in ('jp','fr','de','it','no','es','se','gb','ca','us','au','nz','nl','bg'):
            req = "{0}('{1}', '{2}', '0', '0', '', ''),".format(req, ip,country)
            try:
        
             cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",'spoti')
             cmd = "INSERT INTO proxies2(proxie_port, country, in_use, error, user, password) VALUES {}".format(req)
             cmd = cmd[:-1]
             cursor = cnx.cursor()
             cursor.execute(cmd)
             cnx.commit() 
             i=i+1
             print("inserted : " + str(myip1) )
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
             print("inserted : " + str(proxy) )
           except:
             err=1

        
      
    except:
      err=1
       
    
	  
 print("wait()")
 sleep(30)
  