from urllib.parse import quote as _quote
from .utils import to_json

class Route:
    base = "https://discord.com/api/v9"

    def __init__(self, method, path, **params):
        self.method = method
        self.path = path
        self.raw_path = path
        if params:
            self.path = self.path.format_map({k: _quote(v) if isinstance(v, str) else v for k, v in params.items()})
        self.url = self.base + self.path
        self._bucket = None
        self.major_params = {k:v for k, v in params.items() if k in ('channel_id', 'guild_id', 'webhook_id', 'webhook_token')}

    @property
    def bucket(self):
        return self._bucket or f"{self.method}:{self.raw_path}:" + ":".join([str(i) for i in self.major_params.values()])

    def __eq__(self, other):
        return (
            isinstance(other, Route) and
            other.path == self.path and
            other.method == self.method and
            other.major_params == self.major_params
        )

    def __hash__(self):
        return hash(self.url+to_json(self.major_params))
