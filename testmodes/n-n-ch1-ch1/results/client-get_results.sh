#!/bin/bash
FILES=../client/iperf/*
for f in $FILES
do
	filename=$(basename $f)
	cat $f | grep sec | head -$(cat $f | wc -l) | tr - " " | awk '{print $3,$8}' | head -n -1 > $filename
	#bash continous_time.sh $filename
	#echo "This is file $f"
done
