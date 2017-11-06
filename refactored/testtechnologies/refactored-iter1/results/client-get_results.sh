#!/bin/bash

<<'COMMENT'
MPTCP performance test
created by:
Grzegorz Przybylo
University of Science and Technology in Cracow
Faculty of Computer Science, Electronics and Telecomunications
ICT
COMMENT

FILES=../client/iperf/*
for f in $FILES
do
	filename=$(basename $f)
	cat $f | grep sec | head -$(cat $f | wc -l) | tr - " " | awk '{print $3,$8}' | head -n -1 > $filename
done
