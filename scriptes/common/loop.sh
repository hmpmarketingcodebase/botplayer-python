while true
do
   sudo killall chrome chromedriver
   sleep 5s
   sudo bash clean_ram.sh
   sleep 5s
   sudo bash clean_tmp.sh
   sleep 7000s   
done
