#!/bin/bash
#sched=$(cat /proc/sys/net/mptcp/mptcp_scheduler)
#pm=$(cat /proc/sys/net/mptcp/mptcp_path_manager)
echo "Running iperf server for scheduler $1 and path manager $2"
iperf -s -i 1 > ../server/server_$1_$2
