while true
do
   python3 spotify.py $1 $2 $3 $4 $5 & disown
   sleep 12h
   killall python3 Xvfb chrome chromedriver
   sleep 120s
done
