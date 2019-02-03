while true
do
   sudo killall python3 Xvfb chrome chromedriver
   sleep 60s
   nohup python3 spotify2.py 0</dev/null &  
   sleep 14400s
done
==============