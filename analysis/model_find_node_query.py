from datetime import datetime
from typing import Optional, List

from dht.model_peer import Peer


class FindNodeQuery:
    cid: str

    target_peer: Peer
    started_at: datetime

    ended_at: Optional[datetime]
    closest_peers: Optional[List[Peer]]
    error_str: Optional[str]

    def __init__(self, target_peer: Peer, cid: str, started_at: datetime) -> None:
        self.cid = cid
        self.started_at = started_at
        self.target_peer = target_peer
        self.closest_peers = None
        self.error_str = None

    def succeeded(self, ended_at: datetime, closest_peers: List[Peer]):
        if self.is_done:
            print(f"cid {self.cid} find node query already done {self.target_peer}")
            return
        self.ended_at = ended_at
        self.closest_peers = closest_peers

    def failed(self, ended_at: datetime, error_str):
        if self.is_done:
            print(f"cid {self.cid} find node query already done {self.target_peer}")
            return
        self.ended_at = ended_at
        self.error_str = error_str

    @property
    def is_done(self):
        return self.error_str is not None or self.closest_peers is not None
