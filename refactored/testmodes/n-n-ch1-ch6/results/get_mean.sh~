#!/bin/bash
FILES=client_*
for f in $FILES
do
	filename=$(basename $f)
	bash calcMean.sh $filename >> meanResults.txt
done
