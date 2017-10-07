#!/bin/bash
awk '{ total += $2 } END { print "AVG for file: "FILENAME,total/NR }' $1
