import pickle
from typing import Tuple, Dict
from dht.model_publication import Publication
from dht.model_retrieval import Retrieval
import sys
import dht.model_publication
import dht.model_peer
import dht.model_closest_peers_query
import dht.model_provider_query
import dht.model_retrieval
import dht.model_get_providers_query

sys.modules['model_publication'] = dht.model_publication
sys.modules['model_peer'] = dht.model_peer
sys.modules['model_closest_peers_query'] = dht.model_closest_peers_query
sys.modules['model_provider_query'] = dht.model_provider_query
sys.modules['model_retrieval'] = dht.model_retrieval
sys.modules['model_get_providers_query'] = dht.model_get_providers_query

def load(file_name) -> Tuple[Dict[str, Publication], Dict[str, Retrieval]]:
    with open(file_name, "rb") as f:
        return pickle.load(f)
