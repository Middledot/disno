"""
MIT License

Copyright (c) 2021-present Qwire Development Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from ..route import Route
from ..utils import bytes_to_base64_data, MISSING


class TemplateEndpoints:
    def get_template(self, code: str):
        r = Route("GET", "/guilds/templates/{code}", code=code)
        return self.request(r)

    def create_guild_from_template(self, code: str, *, name: str, icon: bytes = None):
        r = Route("POST", "/guilds/templates/{code}", code=code)
        payload = {
            "name": name,
        }

        if icon is not None:
            payload["icon"] = bytes_to_base64_data(icon)

        return self.request(r, payload=payload)

    def get_guild_templates(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/templates", guild_id=guild_id)
        return self.request(r)

    def sync_template(self, guild_id: int, code: str):
        r = Route("PUT", "/guilds/{guild_id}/templates/{code}", guild_id=guild_id, code=code)
        return self.request(r)

    def create_template(self, guild_id: int, *, name: str, description: str = None):
        r = Route("POST", "/guilds/{guild_id}/templates", guild_id=guild_id)
        payload = {
            "name": name,
        }

        if description is not None:
            payload["description"] = description

        return self.request(r, payload=payload)

    def edit_template(self, guild_id: int, code: str, *, name: str = MISSING, description: str = MISSING):
        r = Route("PATCH", "/guilds/{guild_id}/templates/{code}", guild_id=guild_id, code=code)
        payload = {}

        if name is not MISSING:
            payload["name"] = name

        if description is not MISSING:
            payload["description"] = description

        return self.request(r, payload=payload)

    def delete_template(self, guild_id: int, code: str):
        r = Route("POST", "/guilds/{guild_id}/templates/{code}", guild_id=guild_id, code=code)
        return self.request(r)
