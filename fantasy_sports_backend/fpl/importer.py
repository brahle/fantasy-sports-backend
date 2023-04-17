from os import environ
from typing import Any, Optional, Type, TypeVar

from brds import Importer
from requests import Response, session
from requests.exceptions import HTTPError
from requests.sessions import Session

T = TypeVar("T", bound="FantasyPremierLeagueImporter")


class FantasyPremierLeagueImporter(Importer):
    def __init__(self: "FantasyPremierLeagueImporter") -> None:
        self._session: Optional[Session] = None

    def _get(
        self: "FantasyPremierLeagueImporter", *args: Any, **kwargs: Any
    ) -> Response:
        try:
            r = self.session.get(*args, **kwargs)
            r.raise_for_status()
            return r
        except HTTPError as err:
            raise SystemExit(err)

    def get(self: "FantasyPremierLeagueImporter", url: str) -> Any:
        if url == "fantasy":
            return self._get(
                f"https://fantasy.premierleague.com/api/bootstrap-static/"
            ).json()
        return self._get(f"https://draft.premierleague.com/api/{url}").json()

    @classmethod
    def from_environment(cls: Type[T]) -> T:
        return cls()

    @property
    def session(self: "FantasyPremierLeagueImporter") -> Session:
        if self._session is None:
            self._session = session()
        return self._session
