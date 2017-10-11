#!/bin/bash
FILES=../client2/iperf/*
for f in $FILES
do
	filename=$(basename $f)
	cat $f | grep sec | head -$(cat $f | wc -l) | tr - " " | awk '{print $3,$8}' | head -n -1 > client2/$filename
	#bash continous_time.sh $filename
	#echo "This is file $f"
done
