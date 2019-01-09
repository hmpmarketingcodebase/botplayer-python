depth=0;
while true
do
   sudo bash clean_tmp.sh
   sleep 1000s
   sudo bash clean_ram.sh
   sleep 1000s
   
   let "depth++"
   if [ `expr $depth % 5` -eq 0 ]; then
   sudo killall chrome chromedriver
   fi
done
