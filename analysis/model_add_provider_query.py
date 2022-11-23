from datetime import datetime
from model_peer import Peer
from typing import Optional


class AddProviderQuery:
    cid: str
    target_peer: Peer
    started_at: datetime
    ended_at: Optional[datetime]
    success: Optional[bool]
    errors: Optional[str]

    def __init__(self, target_peer: Peer, cid: str, started_at: datetime) -> None:
        self.cid = cid
        self.started_at = started_at
        self.target_peer = target_peer
        self.ended_at = None
        self.success = None
        self.errors = None

    def succeeded(self, ended_at: datetime):
        if self.is_done:
            raise Exception(f"cid {self.cid} add provider query already done {self.target_peer}")
        self.ended_at = ended_at
        self.success = True

    def failed(self, ended_at: datetime, errors: str):
        if self.is_done:
            raise Exception(f"cid {self.cid} add provider query already done {self.target_peer}")
        self.ended_at = ended_at
        self.success = False
        self.errors = errors

    @property
    def is_done(self) -> bool:
        return self.success is not None
