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


class InviteEndpoints:
    def get_vanity_invite(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/vanity-url", guild_id=guild_id)
        return self.request(r)

    def get_invite(self, code: str):
        r = Route("GET", "/invites/{code}", code=code)
        return self.request(r)

    def get_invites(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/invites", guild_id=guild_id)
        return self.request(r)

    def get_channel_invites(self, channel_id: int):
        r = Route('GET', '/channels/{channel_id}/invites', channel_id=channel_id)
        return self.request(r)

    def create_invite(
        self,
        channel_id: int,
        *,
        max_age: int,
        max_uses: int,
        temporary: bool,
        unique: bool,
        target_type: int,
        target_user_id: int,
        target_application_id: int,
        reason: str = None
    ):
        r = Route('POST', '/channels/{channel_id}/invites', channel_id=channel_id)
        payload = {
            "max_age": max_age,
            "max_uses": max_uses,
            "temporary": int(temporary),
            "unique": int(unique),
            "target_type": target_type,
            "target_user_id": target_user_id,
            "target_application_id": target_application_id,
        }

        return self.request(r, payload=payload, reason=reason)

    def delete_invite(self, code: str, *, reason: str = None):
        r = Route("DELETE", "/invites/{code}", code=code)
        return self.request(r, reason=reason)
