while true
do
   sudo killall python3 Xvfb chrome chromedriver
   sleep 5s
   sudo chgrp -R coramelevivgame .
   sleep 5s
   sudo chmod -R ug+w .;
   sleep 5s
   git config --global user.email 'zzakariaa10@yahoo.fr' & disown
   sleep 5s
   git config --global user.name 'Zak' & disown
   sleep 5s
   git stash save --keep-index & disown
   sleep 5s
   git pull origin master & disown
   sleep 5s
   sudo chmod -R 777 * & disown
   sleep 10s
    
   python3 spotify.py $1 $2 $3 $4 $5 & disown 
   sleep 4h
   sudo killall python3 Xvfb chrome chromedriver
   sleep 120s
done
