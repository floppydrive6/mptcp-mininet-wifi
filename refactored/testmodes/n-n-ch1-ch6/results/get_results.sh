#!/bin/bash

<<'COMMENT'
MPTCP performance test
created by:
Grzegorz Przybylo
University of Science and Technology in Cracow
Faculty of Computer Science, Electronics and Telecomunications
ICT
COMMENT

FILES=../server/*
for f in $FILES
do
	filename=$(basename $f)
	cat $f | grep sec | head -60 | tr - " " | awk '{print $3,$8}' > $filename
	#bash continous_time.sh $filename
	#echo "This is file $f"
done
