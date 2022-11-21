from datetime import datetime
from dht.model_peer import Peer
from typing import Optional, List


class GetProvidersQuery:
    cid: str
    target_peer: Peer
    started_at: datetime

    ended_at: Optional[datetime]
    closer_peers: Optional[List[Peer]]
    providers_count: Optional[int]
    error_str: Optional[str]

    def __init__(self, target_peer: Peer, cid: str, started_at: datetime) -> None:
        self.cid = cid
        self.started_at = started_at
        self.target_peer = target_peer
        self.providers_count = None
        self.ended_at = None
        self.closer_peers = None

    def succeeded(self, ended_at: datetime, closer_peers: List[Peer], providers_count: int):
        if self.ended_at is None or self.ended_at > ended_at:
            self.ended_at = ended_at
        if self.closer_peers is None or len(closer_peers) > len(self.closer_peers):
            self.closer_peers = closer_peers
        if self.providers_count is None or providers_count > self.providers_count:
            self.providers_count = providers_count

    def failed(self, ended_at: datetime, error_str: Optional[str]):
        self.ended_at = ended_at
        self.error_str = error_str

    @property
    def is_done(self):
        return self.ended_at is not None
