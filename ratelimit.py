import datetime
import requests


class RateLimit:
    def __init__(self, resp: requests.Response = None):
        self.__limit: int | None = None
        self.__remaining: int | None = None
        self.__reset: datetime.datetime | None = None

        if resp:
            self.update(resp)

    @property
    def limit(self):
        return self.__limit

    @property
    def remaining(self):
        return self.__remaining

    @property
    def reset(self):
        return self.__reset

    def update(self, resp: requests.Response):
        self.__limit = resp.headers.get('X-Ratelimit-Limit', None)
        self.__remaining = resp.headers.get('X-Ratelimit-Remaining', None)
        self.__reset = datetime.datetime.fromtimestamp(int(resp.headers.get('X-Ratelimit-Reset', 0)))
