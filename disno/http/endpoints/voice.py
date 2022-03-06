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
from ..utils import MISSING


class VoiceEndpoints:
    def list_voice_regions(self):
        r = Route("GET", "/voice/regions")
        return self.request(r)

    def get_voice_regions(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/regions", guild_id=guild_id)
        return self.request(r)

    def edit_current_user_voice_state(self, guild_id: int, *, channel_id: int, suppress: bool = MISSING, request_to_speak_timestamp: str = MISSING):
        # TODO: test if channel_id is actually required
        r = Route("PATCH", "/guilds/{guild_id}/voice-states/@me", guild_id=guild_id)
        payload = {"channel_id": channel_id}

        if suppress is not MISSING:
            payload["suppress"] = suppress

        if request_to_speak_timestamp is not MISSING:
            payload["request_to_speak_timestamp"] = request_to_speak_timestamp

        return self.request(r, payload=payload)

    def edit_user_voice_state(self, guild_id: int, user_id: int, *, channel_id: int, suppress: bool = MISSING):
        r = Route("PATCH", "/guilds/{guild_id}/voice-states/{user_id}", guild_id=guild_id, user_id=user_id)
        payload = {"channel_id": channel_id}

        if suppress is not MISSING:
            payload["suppress"] = suppress

        return self.request(r, payload=payload)
