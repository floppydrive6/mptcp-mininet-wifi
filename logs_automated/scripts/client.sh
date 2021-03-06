#!/bin/bash
#sched=$(cat /proc/sys/net/mptcp/mptcp_scheduler)
#pm=$(cat /proc/sys/net/mptcp/mptcp_path_manager)
echo "Running client for $1 scheduler and $2 path manager"
number=20
for (( c=0; c<$number; c++ ))
do
	echo $((c+1))" repetition of running iperf"
	iperf -c 192.168.1.254 -t 10 > ../client/client_$1_$2_$((c+1))
	sleep 5
done
