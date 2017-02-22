#!/bin/bash
n=0
for i in $(seq 1 4)
do
    min=$n
    n=$(($n+500000))
    max=$n
    echo "round $i"
    echo $min
    echo $max
    python3 classify_countries.py $min $max &
done
