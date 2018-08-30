while true
do
   python3 spotify.py spot_test4 $1 $2 $3 $4 & disown
   sleep 25s
   killall python3 Xvfb chrome chromedriver
   sleep 6s
done
