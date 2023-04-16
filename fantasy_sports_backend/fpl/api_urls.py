from dataclasses import dataclass
from typing import Union


@dataclass
class Config:
    """Configuration of the FPL settings."""

    league_id: int
    file_prefix: str = "premierleague.com/"


class ApiUrls:
    def __init__(self: "ApiUrls", config: Config) -> None:
        self.config = config

    def __getattr__(self: "ApiUrls", name: str) -> str:
        assert name.endswith("_file"), "'{name}' - unknown attribute."
        return f"{self.config.file_prefix}{self.__getattribute__(name[:-5])}"

    @property
    def draft_choices(self: "ApiUrls") -> str:
        """URL for getting currently selected draft choices."""
        return f"draft/{self.config.league_id}/choices"

    @property
    def bootstrap_static(self: "ApiUrls") -> str:
        return "bootstrap-static"

    @property
    def league_element_status(self: "ApiUrls") -> str:
        return f"league/{self.config.league_id}/element-status"

    @property
    def league_details(self: "ApiUrls") -> str:
        return f"league/{self.config.league_id}/details"

    @property
    def fantasy(self: "ApiUrls") -> str:
        return "fantasy"

    @property
    def league_transactions(self: "ApiUrls") -> str:
        return f"draft/league/{self.config.league_id}/transactions"

    @property
    def league_trades(self: "ApiUrls") -> str:
        return f"draft/league/{self.config.league_id}/trades"

    @property
    def league_score_history(self: "ApiUrls") -> str:
        return f"league/{self.config.league_id}/score_history"

    def entry_history(self: "ApiUrls", entry_id: Union[int, str]) -> str:
        return f"entry/{entry_id}/history"

    def entry_history_file(self: "ApiUrls", entry_id: Union[int, str]) -> str:
        return f"{self.config.file_prefix}entry/{entry_id}/history"
