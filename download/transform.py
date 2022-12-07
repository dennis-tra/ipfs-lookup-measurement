import json


def run():
    with open("nodes-list-fleet-1-node-1-plain.log") as f:
        lines = reversed(f.readlines())

    with open("../data/2022-12-05_hydra_dial_down/nodes-list-fleet-1-node-1.log", "w") as f:
        for line in lines:
            data = {
                "labels": {},
                "line": line.rstrip("\n"),
                "timestamp": "-"
            }
            f.write(json.dumps(data) + "\n")


if __name__ == "__main__":
    run()
