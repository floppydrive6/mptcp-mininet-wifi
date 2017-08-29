#!/bin/bash
SCHEDULER=$(cat data/scheduler.txt)
PATH_MANAGER=$(cat data/path_manager.txt)
bash client.sh $SCHEDULER $PATH_MANAGER
