from urllib.request import Request, urlopen
import MySQLdb
import requests
from time import sleep
while 1:
 i=0
 cnx = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",'spoti') 
 curs = cnx.cursor()
 curs.execute("select * from proxies2 where error = 0")
 prox = curs.fetchall()
 file1 = open("t.txt","w")
 ii=0

 for ipss in prox:
    try: 
      ii+=1
      print(str(i))
      ip = ipss[1]
      i=i+1
      ip=str(ip).replace("\n","")
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
      myip = myip+"#"+country


      #$country = substr($ips[0], strlen($ips[0]) - 4, 2);
      if("dead" in str(myip)):
         print(str(i) + " > " + str(myip) );
         cnx2 = MySQLdb.connect("52.17.67.92","user",",Dc7aUb)3t>H@1.",'spoti') 
         curs2 = cnx2.cursor()
         curs2.execute("delete from proxies2 where id = '"+str(ipss[0])+"'")
         cnx2.commit()
         
 
      file1.write(myip)
       
    except:
      err=0
	  
 print("wait()")
 sleep(60)
  