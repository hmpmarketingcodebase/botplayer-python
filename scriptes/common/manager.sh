#!/bin/sh
t=0
while true
do
num=$(df -h | awk '$NF=="/"{printf "%s", $5}')
disk=$num

if [ "$disk" = "100%" ]
then
echo "Clean DISK"
nohup sudo bash clean_tmp.sh 0</dev/null &
nohup sudo killall python3 chrome chromedriver Xvfb 0</dev/null &

sleep 30s

nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &

fi

echo "DISK "${disk}
if [ ${disk} \> "95%" ]
then
echo "Clean DISK"
nohup sudo bash clean_tmp.sh 0</dev/null &
nohup sudo killall python3 chrome chromedriver Xvfb 0</dev/null &

sleep 30s

nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &

fi

num=$(free -m | awk 'NR==2{printf "%.f", $3*100/$2 }')
ram=$(($num))
echo "RAM "${ram}"%"
if (( $(($ram)) > 84 ))
then
echo "clean RAM"
nohup sudo bash clean_ram.sh 0</dev/null &
nohup sudo killall python3 chrome chromedriver Xvfb 0</dev/null &

sleep 30s

nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &

fi

sleep 5s

num=$(free -m | awk 'NR==2{printf "%.f", $3*100/$2 }')
ram=$(($num))
if (( $(($ram)) > 84 ))
then
echo "RAM "${ram}"%"
echo "KILLALL"

nohup sudo killall python3 chrome chromedriver Xvfb 0</dev/null &

sleep 30s

nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
nohup python3 ../spotify/$1 0</dev/null &
fi
num=$(df -h | awk '$NF=="/"{printf "%s", $5}')
hr=$(date +"%H")
if((${t}==0))
then
   if(($(($hr)) == 0))
   then
   nohup sudo killall python3 chrome chromedriver Xvfb 0</dev/null &
   sleep 30s
   echo "start script"
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   t=1
   fi
fi
if((${t}==1))
then
   if(($(($hr)) == 12))
   then
   nohup sudo killall python3 chrome chromedriver Xvfb 0</dev/null &
   sleep 30s
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   nohup python3 ../spotify/$1 0</dev/null &
   t=0
   fi
fi
done
