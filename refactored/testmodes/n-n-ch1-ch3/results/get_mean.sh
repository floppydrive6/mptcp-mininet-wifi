#!/bin/bash

<<'COMMENT'
MPTCP performance test
created by:
Grzegorz Przybylo
University of Science and Technology in Cracow
Faculty of Computer Science, Electronics and Telecomunications
ICT
COMMENT

FILES=client_*
for f in $FILES
do
	filename=$(basename $f)
	bash calcMean.sh $filename >> meanResults.txt
done
