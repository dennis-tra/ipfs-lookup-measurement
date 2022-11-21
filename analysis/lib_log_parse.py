import pickle
from datetime import datetime
from typing import List

from dht.model_log_file import LogFile
from dht.model_publication import Publication
from dht.model_retrieval import Retrieval


class ParsedLogFile:
    def __init__(
            self,
            publications: List[Publication],
            retrievals: List[Retrieval],
            unattempted_retrieval_cids: List[str]):
        self.publications: List[Publication] = publications
        self.retrievals: List[Retrieval] = retrievals
        self.unattempted_retrieval_cids: List[str] = unattempted_retrieval_cids


def load_parsed_logs(log_files: List[str]) -> List[ParsedLogFile]:
    parsed_logs: List[ParsedLogFile] = []
    for log_file in log_files:
        start = datetime.now()
        with open(log_file + ".p", "rb") as f:
            print("Loading ", log_file)
            plf: ParsedLogFile = pickle.load(f)
            print(f"Took {datetime.now() - start}")
            parsed_logs += [plf]
    return parsed_logs


def parse(log_files: List[str]) -> List[ParsedLogFile]:
    plfs = []
    for log_file in log_files:
        parsed = LogFile.parse(log_file)
        plf = ParsedLogFile(list(parsed[0].values()), list(parsed[1].values()), parsed[2])
        plfs += [plf]
        with open(log_file + ".p", "wb") as f:
            pickle.dump(plf, f)
    return plfs


if __name__ == '__main__':
    logs = [
        "./dht/2022-01-16-data/0.log",
        "./dht/2022-01-16-data/1.log",
        "./dht/2022-01-16-data/2.log",
        "./dht/2022-01-16-data/3.log",
        "./dht/2022-01-16-data/4.log",
        "./dht/2022-01-16-data/5.log",
    ]
    # load_parsed_logs(logs)
    parse(logs)
