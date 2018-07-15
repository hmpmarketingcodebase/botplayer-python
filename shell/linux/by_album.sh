#!/bin/sh
cd ..
cd ..
nohup python3 ./python_files/by_album.py $1 $2 $3 $4 </dev/null &
