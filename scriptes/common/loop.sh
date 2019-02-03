while true
do
   sleep 5s
   sudo bash clean_ram.sh
   sleep 5s
   sudo bash clean_tmp.sh
   sleep 3600s   
done
