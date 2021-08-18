import requests
from js2py.internals import seval


class LeaderboardClient:

    def __init__(self):
        self.session = requests.Session()
        self.user_tracking_id = self._set_tracking_user_id()

    def _set_tracking_user_id(self):
        js = self.session.get("https://microservice.pgatour.com/js").text
        return seval.eval_js_vm(f"window = {{}}; {js}; window.pgatour.setTrackingUserId('id8730931');")
