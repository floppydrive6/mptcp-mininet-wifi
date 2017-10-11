#!/bin/bash
FILES=../client2/client_*
for FILE in $FILES; do
	filename=$(basename $FILE)
	gnuplot <<- EOF
		set terminal png
		set tics font "Helvetica,10"
		set ylabel "Mbit/s"
		set xlabel "s"
		set output "plots/client2/${filename}.png"
		plot "${FILE}" title "${FILE}" with linespoints
EOF
done
