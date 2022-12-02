import json

with open("nodes-list-fleet-2-node-5-plain.log") as f:
    lines = reversed(f.readlines())

with open("../data/2022-12-02_hydra_dial_down/nodes-list-fleet-2-node-5.log", "w") as f:
    for line in lines:
        data = {
            "labels": {},
            "line": line.rstrip("\n"),
            "timestamp": "-"
        }
        f.write(json.dumps(data)+"\n")
