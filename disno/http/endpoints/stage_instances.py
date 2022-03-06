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


class StageInstanceEndpoints:
    def create_stage_instance(self, *, channel_id: int, topic: str, privacy_level: int = None, reason: str = None):
        r = Route("POST", "/stage-instances")
        payload = {
            "channel_id": channel_id,
            "topic": topic,
        }

        if privacy_level is not None:
            payload["privacy_level"] = privacy_level

        return self.request(r, payload=payload, reason=reason)

    def get_stage_instance(self, channel_id: int):
        r = Route("GET", "/stage-instances/{channel_id}", channel_id=channel_id)
        return self.request(r)

    def edit_stage_instance(self, channel_id: int, *, topic: str = MISSING, privacy_level: int = MISSING, reason: str = None):
        r = Route("PATCH", "/stage-instances/{channel_id}", channel_id=channel_id)
        payload = {}

        if topic is not MISSING:
            payload["topic"] = topic

        if privacy_level is not MISSING:
            payload["privacy_level"] = privacy_level

        return self.request(r, payload=payload, reason=reason)

    def delete_stage_instance(self, channel_id: int, *, reason: str = None):
        r = Route("DELETE", "/stage-instances/{channel_id}", channel_id=channel_id)
        return self.request(r, reason=reason)
