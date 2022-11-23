import durationpy
from enum import Enum
from datetime import datetime, timedelta

from model_add_provider_query import AddProviderQuery
from model_get_providers_query import GetProvidersQuery
from model_peer import Peer
from model_find_node_query import FindNodeQuery

from typing import Optional, List, Dict


class Publication:
    class State(Enum):
        INITIATED = 1
        GETTING_CLOSEST_PEERS = 2
        PUTTING_GETTING_PROVIDER_RECORDS = 3
        DONE = 4

    _state: State

    # The filename of the log file this publication came from
    origin: str
    # The content identifier that node provided
    cid: str
    invalid: bool

    # When did we start the process of publishing the CID
    provide_started_at: datetime
    # When did we start the first query to get the closest peers for the above CID
    find_node_started_at: Optional[datetime]
    # When have we found the 20 closest peers for the above CID
    dht_walk_ended_at: Optional[datetime]
    # When have all put operations finished
    provide_ended_at: Optional[datetime]
    # When did the checks for stored provider records end at
    get_providers_ended_at: Optional[datetime]

    closest_peers: Optional[List[Peer]]

    # All performed queries for the closest peers
    find_node_queries: List[FindNodeQuery]
    # All add provider RPCs and their outcomes
    add_provider_queries: Dict[Peer, AddProviderQuery]
    # All get provider RPCs and their outcomes
    get_provider_queries: Dict[Peer, GetProvidersQuery]

    def __init__(self, origin: str, cid: str, publication_started_at: datetime) -> None:
        self.origin = origin
        self.cid = cid
        self.provide_started_at = publication_started_at
        self._state = Publication.State.INITIATED
        self.find_node_queries = []
        self.add_provider_queries = {}
        self.get_provider_queries = {}
        self.closest_peers = None
        self.invalid = False

    def duration_total_publication(self) -> timedelta:
        # The duration of the complete provide operation. This includes
        # walking the DHT until we find the appropriate peers and then
        # actually storing the records at them
        return self.provide_ended_at - self.provide_started_at

    def duration_dht_walk(self) -> timedelta:
        # The time it took to find the 20 closest peers. At this point we
        # haven't put the provider record at them yet.
        return self.dht_walk_ended_at - self.provide_started_at

    def duration_total_add_provider(self) -> timedelta:
        # The duration to perform all ADD_PROVIDER RPCs regardless of errors
        return self.provide_ended_at - self.dht_walk_ended_at

    def durations_add_provider_success(self) -> List[timedelta]:
        # The latencies it took to perform the ADD_PROVIDER RPC in case it succeeded
        latencies: List[timedelta] = []
        for query in self.add_provider_queries.values():
            if not query.success:
                continue
            latencies.append(durationpy.from_str(query.time_taken).total_seconds())
        return latencies

    def durations_add_provider_error(self) -> List[timedelta]:
        # The latencies it took to perform the ADD_PROVIDER RPC in case it failed
        latencies: List[timedelta] = []
        for query in self.add_provider_queries.values():
            if query.success:
                continue
            latencies.append(durationpy.from_str(query.time_taken).total_seconds())
        return latencies

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if self._state == state:
            return
        elif self._state == Publication.State.INITIATED and state == Publication.State.GETTING_CLOSEST_PEERS:
            self._state = state
        elif self._state == Publication.State.GETTING_CLOSEST_PEERS and state == Publication.State.PUTTING_GETTING_PROVIDER_RECORDS:
            self._state = state
        elif self._state == Publication.State.PUTTING_GETTING_PROVIDER_RECORDS and state == Publication.State.DONE:
            self._state = state
        else:
            raise Exception(f"Illegal state transition from {self._state} to {state}")

    def getting_closest_peers_started(self, timestamp: datetime):
        self.state = Publication.State.GETTING_CLOSEST_PEERS
        self.find_node_started_at = timestamp

    def find_node_query_started(self, target_peer: Peer, timestamp: datetime):
        self.find_node_queries += [FindNodeQuery(target_peer, self.cid, timestamp)]

    def find_node_query_ended(self, target_peer: Peer, timestamp: datetime, closest_peers: Optional[List[Peer]],
                              error_str: Optional[str] = None):
        if self.invalid:
            return
        for query in reversed(self.find_node_queries):
            if target_peer == query.target_peer:
                if error_str is None:
                    query.succeeded(timestamp, closest_peers)
                else:
                    query.failed(timestamp, error_str)
                return
        print(f"Unstarted query ended CID: {self.cid} target peer: {target_peer.id}")
        self.invalid = True

    def dht_walk_ended(self, timestamp: datetime, closest_peers: List[Peer]):
        self.state = Publication.State.PUTTING_GETTING_PROVIDER_RECORDS
        self.dht_walk_ended_at = timestamp

        # Stop all FIND_NODE queries
        for query in self.find_node_queries:
            if not query.is_done:
                query.failed(timestamp, "cancelled")

        self.closest_peers = closest_peers

    def add_provider_started(self, target_peer: Peer, timestamp: datetime):
        if target_peer in self.add_provider_queries:
            print(f"Added provider record to peer {target_peer} for cid {self.cid} multiple times")
            return
        self.add_provider_queries[target_peer] = AddProviderQuery(target_peer, self.cid, timestamp)

    def add_provider_error(self, peer: Peer, timestamp: datetime, errors: str):
        if peer not in self.add_provider_queries:
            raise Exception(f"Peer {peer.id} is not in the closest peer list for {self.cid}")
        self.add_provider_queries[peer].failed(timestamp, errors)
        if self.is_putting_done():
            self.provide_ended_at = timestamp

    def add_provider_success(self, peer: Peer, timestamp: datetime):
        if peer not in self.add_provider_queries:
            raise Exception(f"Peer {peer.id} is not in the closest peer list for {self.cid}")
        self.add_provider_queries[peer].succeeded(timestamp)

        if self.is_putting_done():
            self.provide_ended_at = timestamp

        self.get_provider_queries[peer] = GetProvidersQuery(peer, self.cid, timestamp)

    def is_putting_done(self):
        if len(self.add_provider_queries) != len(self.closest_peers):
            return

        for peer in self.add_provider_queries:
            if not self.add_provider_queries[peer].is_done:
                return False
        return True

    def get_provider_success(self, peer: Peer, timestamp: datetime):
        if peer not in self.get_provider_queries:
            raise Exception(f"Peer {peer.id} is not in the succeeded put providers list for {self.cid}")
        self.get_provider_queries[peer].succeeded(timestamp, [], 1)

    def get_provider_error(self, peer: Peer, timestamp: datetime, error: str):
        if peer not in self.get_provider_queries:
            raise Exception(f"Peer {peer.id} is not in the succeeded put providers list for {self.cid}")
        self.get_provider_queries[peer].failed(timestamp, error)

    def seal(self, timestamp: datetime):
        self.get_providers_ended_at = timestamp
        self.state = Publication.State.DONE

        expected_get_queries = 0
        for peer in self.add_provider_queries:
            query = self.add_provider_queries[peer]
            if query.success:
                expected_get_queries += 1

        if len(self.get_provider_queries) != expected_get_queries:
            raise Exception(
                f"expected {expected_get_queries} but performed {len(self.get_provider_queries)} get queries for cid {self.cid}")
