while true
do
   sudo bash clean_tmp.sh
   sleep 5s
   sudo bash clean_ram.sh
   sleep 5s
   sudo killall chrome chromedriver
   sleep 7200s   
done
