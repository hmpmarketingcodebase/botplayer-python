while true
do
   python3 spotify.py $1 $2 $3 $4 $5 & disown
   sleep 25s
   killall python3 Xvfb chrome chromedriver
   sleep 6s
done
