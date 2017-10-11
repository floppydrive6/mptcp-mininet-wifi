#!/bin/bash
FILES=../server/*
for f in $FILES
do
	filename=$(basename $f)
	cat $f | grep sec | head -60 | tr - " " | awk '{print $3,$8}' > $filename
	#bash continous_time.sh $filename
	#echo "This is file $f"
done
