#!/bin/sh
cd ..
cd ..
nohup python3 ./python_files/by_playlist.py $1 $2 $3 $4 $5 </dev/null &
