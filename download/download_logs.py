#!/usr/bin/env python3

import os
import sys
from subprocess import run


def download_logs(nodes_list, outfile):
    nodes = []
    with open(nodes_list, "r") as f:
        for line in f.readlines():
            if line.startswith("monitor_ip"):
                monitor_ip = line[14:-2]
                print(monitor_ip)
                os.putenv("LOKI_ADDR", f"http://{monitor_ip}:3100/")
            elif line.startswith("node_"):
                nodes += [line[5]]
    
    for node in nodes:
        cmd = """logcli query --limit=987654321 --since=72h --output=jsonl '{host="node%s"}' > %s-node-%s.log """ % (
            node, outfile, node)
        run(cmd, shell=True)




if __name__ == "__main__":
    download_logs(sys.argv[1], sys.argv[2])
