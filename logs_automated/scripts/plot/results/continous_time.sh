#!/bin/bash
awk '{print NR-1 " " $2}' $1 > continous/$1-mod
