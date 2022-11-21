class Peer:
    id: str
    agent_version: str

    def __init__(self, id: str, agent_version: str) -> None:
        self.id = id
        self.agent_version = agent_version

    def __eq__(self, other):
        return hasattr(other, 'id') and self.id == other.id and \
               hasattr(other, 'agent_version')

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.id} ({self.agent_version})"
