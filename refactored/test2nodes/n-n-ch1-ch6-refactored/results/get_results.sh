#!/bin/bash
FILES=../server/*
for f in $FILES
do
	filename=$(basename $f)
	cat $f | grep sec | head -60 | tr - " " | awk '{print $3,$8}' > $filename
done
