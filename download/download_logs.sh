#!/usr/bin/env bash

IFS=$'\n'; set -f

for line in $(cat "$1"); do
    node=$(cut -d '=' -f 1 <<< "$line")
    if [ "$node" == "monitor_ip " ]; then
          continue
    fi
    node_num="${node:5:1}"
    ip_address=$(cut -d '=' -f 2 <<< "$line")
    ip_address="${ip_address:2:${#ip_address}-3}"
    echo "Downloading logs for node $node_num..."
    scp "ubuntu@$ip_address:~/all.log" "$1-node-$node_num.logs"
done
unset IFS; set +f