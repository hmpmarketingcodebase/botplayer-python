#!/bin/sh
cd ..
cd ..
nohup python3 ./python_files/by_search.py $1 $2 $3 $4 </dev/null &
