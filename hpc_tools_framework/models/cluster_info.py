from dataclasses import dataclass
from typing import List

@dataclass
class Partition:
    name: str
    nodes: int
    memory: str
    cpus: int

@dataclass
class ClusterInfo:
    partitions: List[Partition]
