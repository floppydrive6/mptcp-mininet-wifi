#!/bin/bash

<<'COMMENT'
MPTCP performance test
created by:
Grzegorz Przybylo
AGH, University of Science and Technology in Cracow
Faculty of Computer Science, Electronics and Telecomunications
ICT
COMMENT

FILES=../client_*
for FILE in $FILES; do
	filename=$(basename $FILE)
	gnuplot <<- EOF
		set terminal png
		set tics font "Helvetica,10"
		set ylabel "Mbit/s"
		set xlabel "s"
		set output "plots/${filename}.png"
		plot "${FILE}" title "${FILE}" with linespoints
EOF
done
