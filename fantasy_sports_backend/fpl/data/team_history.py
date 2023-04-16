from dataclasses import dataclass
from typing import List, Any


@dataclass
class History:
    id: int
    points: int
    total_points: int
    rank: Any
    rank_sort: Any
    event_transfers: int
    points_on_bench: int
    entry: int
    event: int

@dataclass
class Entry:
    event_points: int
    favourite_team: int
    id: int
    league_set: List[int]
    name: str
    overall_points: int
    player_first_name: str
    player_last_name: str
    region_name: str
    region_code_short: str
    region_code_long: str
    started_event: int
    transactions_event: int
    transactions_total: int

@dataclass
class Data:
    history: List[History]
    entry: Entry
