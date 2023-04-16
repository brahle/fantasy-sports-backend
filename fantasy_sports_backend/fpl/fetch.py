from typing import Any, Dict, List

from brds import Fetcher, FileWriter, fload

from fantasy_sports_backend.fpl.importer import FantasyPremierLeagueImporter
from fantasy_sports_backend.fpl.api_urls import ApiUrls, Config
from fantasy_sports_backend.fpl.data.team_history import Data, Entry, History


def fetch_league_score_history(league_id: int) -> List[List[Dict[str, Any]]]:
    """Import FPL data for the specific league."""
    config = Config(league_id=league_id)
    api_urls = ApiUrls(config)
    writer = FileWriter.from_environment(timestamp_col="timestamp")
    fpli = FantasyPremierLeagueImporter()

    def fetch(*urls: str) -> None:
        Fetcher(fpli, writer, list(urls), prefix=config.file_prefix).fetch()

    fetch(api_urls.league_details)
    entries = fload(api_urls.league_details_file)["league_entries"]
    fetch(*[api_urls.entry_history(entry["entry_id"]) for entry in entries])

    data_history = [load_entry_history(api_urls, entry["entry_id"]) for entry in entries]

    score_history: List[List[Dict[str, Any]]] = []
    for week, _ in enumerate(data_history[0].history):
        score_history.append([])
        for data in data_history:
            score_history[-1].append(
                {
                    "name": f"{data.entry.player_first_name} {data.entry.player_last_name}",
                    "value": data.history[week].total_points,
                }
            )
        score_history[-1].sort(key=lambda x: x["value"], reverse=True)
        if len(score_history) == 1:
            score_history.append(score_history[0])
            for player_score in score_history[-1]:
                player_score["value"] = 0

    writer.write_json(api_urls.league_score_history_file, score_history)
    return score_history


def load_entry_history(api_urls: ApiUrls, entry_id: int) -> Data:
    file_name = api_urls.entry_history_file(entry_id)
    data = fload(file_name)
    history_objects = [History(**history_item) for history_item in data["history"]]
    entry_object = Entry(**data["entry"])
    return Data(history=history_objects, entry=entry_object)


if __name__ == "__main__":
    fetch_league_score_history(37606)
