import requests
import logging
from js2py.internals import seval
from typing import Dict, Any


class LeaderboardClient:
    BASE_URL = "https://lbdata.pgatour.com"

    def __init__(self):
        self.session = requests.Session()
        self.user_tracking_id = self._set_tracking_user_id()

    def _set_tracking_user_id(self):
        js = self.session.get("https://microservice.pgatour.com/js").text
        return seval.eval_js_vm(f"window = {{}}; {js}; window.pgatour.setTrackingUserId('id8730931');")

    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        url = f"{endpoint}?userTrackingId={self.user_tracking_id}"
        response = self.session.get(url)

        if response.status_code == 403:
            logging.info(f"Resetting userTrackingId, Status Code: {response.status_code}, Url: {url}")
            self.user_tracking_id = self._set_tracking_user_id()
            return self._make_request(endpoint)

        response.raise_for_status()
        return response.json()

    def leaderboard(self, tour_code: str, schedule_year: int, tournament_id: str) -> Dict[str, Any]:
        endpoint = f"{LeaderboardClient.BASE_URL}/{schedule_year}/{tour_code}/{tournament_id}/leaderboard.json"
        return self._make_request(endpoint)
