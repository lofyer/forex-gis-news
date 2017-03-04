#!/bin/bash
n=0
for i in $(seq 1 1)
do
    min=$n
    n=$(($n+100))
    max=$n
    echo "round $i"
    echo $min
    echo $max
    python3 classify_countries_no_jieba.py $min $max &
done
