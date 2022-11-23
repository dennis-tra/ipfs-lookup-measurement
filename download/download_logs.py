#!/usr/bin/env python3

import os
import sys
from subprocess import run


def download_logs(nodes_list, outfile):
    node_count = 0
    with open(nodes_list, "r") as f:
        for line in f.readlines():
            if line.startswith("monitor_ip"):
                monitor_ip = line[14:-2]
                print(monitor_ip)
                os.putenv("LOKI_ADDR", f"http://{monitor_ip}:3100/")
            elif line.startswith("node_"):
                node_count += 1
    
    for i in range(0, node_count):
        cmd = """logcli query --limit=987654321 --since=2000h --output=jsonl '{host="node%d"}' > %s-node-%d.log """ % (
            i, outfile, i)
        run(cmd, shell=True)




if __name__ == "__main__":
    download_logs(sys.argv[1], sys.argv[2])
