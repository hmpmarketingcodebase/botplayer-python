#!/bin/sh
t=0
while true
do
nohup sudo killall python3 chrome chromedriver Xvfb 0</dev/null &

echo "Clean DISK"
nohup sudo bash clean_tmp.sh 0</dev/null &
sleep 5s
echo "clean RAM"
nohup sudo bash clean_ram.sh 0</dev/null &

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
sleep 8000s

done
