#!/bin/bash
SCHEDULER=$(cat /proc/sys/net/mptcp/mptcp_scheduler)
PATH_MANAGER=$(cat /proc/sys/net/mptcp/mptcp_path_manager)
echo $SCHEDULER > data/scheduler.txt
echo $PATH_MANAGER > data/path_manager.txt
