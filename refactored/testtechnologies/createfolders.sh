#!/bin/bash

<<'COMMENT'
MPTCP performance test
created by:
Grzegorz Przybylo
AGH, University of Science and Technology in Cracow
Faculty of Computer Science, Electronics and Telecomunications
ICT
COMMENT

if [ -z "$1" ]
then
	echo "First arg must be a folder name"
else
	mkdir $1
	cd $1
	mkdir client
	cd client
	mkdir iperf && mkdir ifstat && mkdir proc
	cd ..
	mkdir server
	echo "DONE"
fi
