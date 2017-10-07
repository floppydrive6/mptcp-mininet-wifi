#!/bin/bash
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
