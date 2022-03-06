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

import datetime
from typing import Optional

from ..route import Route
from ..utils import bytes_to_base64_data, MISSING

class ScheduledEventEndpoints:
    def get_scheduled_events(self, guild_id: int, *, with_user_counts: bool = None):
        r = Route("GET", "/guilds/{guild_id}/scheduled-events", guild_id=guild_id)
        params = {}

        if with_user_counts is not None:
            params["with_user_counts"] = int(with_user_counts)

        return self.request(r, params=params)

    def get_scheduled_event(self, guild_id: int, event_id: int, *, with_user_counts: bool = None):
        r = Route("GET", "/guilds/{guild_id}/scheduled-events/{event_id}", guild_id=guild_id, event_id=event_id)
        params = {}

        if with_user_counts is not None:
            params["with_user_counts"] = int(with_user_counts)

        return self.request(r, params=params)

    def create_scheduled_event(
        self,
        guild_id: int,
        *,
        name: str,
        privacy_level: int,
        entity_type: int,
        scheduled_start_time: datetime.datetime,
        scheduled_end_time: datetime.datetime = None,
        description: str = None,
        entity_metadata = None,
        channel_id: str = None,
        image: bytes = None
    ):
        r = Route("POST", "/guilds/{guild_id}/scheduled-events", guild_id=guild_id)
        payload = {
            "name": name,
            "privacy_level": privacy_level,
            "entity_type": entity_type,
            "scheduled_start_time": scheduled_start_time.isoformat()
        }

        if scheduled_end_time is not None:
            payload["scheduled_end_time"] = scheduled_end_time.isoformat()

        if description is not None:
            payload["description"] = description

        if entity_metadata is not None:
            payload["entity_metadata"] = entity_metadata

        if channel_id is not None:
            payload["channel_id"] = channel_id

        if image is not None:
            payload["image"] = bytes_to_base64_data(image)

        return self.request(r, payload=payload)

    def edit_scheduled_event(
        self,
        guild_id: int,
        event_id: int,
        *,
        name: str = MISSING,
        privacy_level: int = MISSING,
        entity_type: int = MISSING,
        scheduled_start_time: datetime.datetime = MISSING,
        scheduled_end_time: datetime.datetime = MISSING,
        description: str = MISSING,
        entity_metadata = MISSING,
        channel_id: str = MISSING,
        image: bytes = MISSING
    ):
        r = Route("POST", "/guilds/{guild_id}/scheduled-events/{event_id}", guild_id=guild_id, event_id=event_id)
        payload = {}

        if name is not MISSING:
            payload["name"] = name

        if privacy_level is not MISSING:
            payload["privacy_level"] = privacy_level

        if entity_type is not MISSING:
            payload["entity_type"] = entity_type

        if scheduled_start_time is not MISSING:
            payload["scheduled_start_time"] = scheduled_start_time.isoformat()

        if scheduled_end_time is not MISSING:
            payload["scheduled_end_time"] = scheduled_end_time.isoformat()

        if description is not MISSING:
            payload["description"] = description

        if entity_metadata is not MISSING:
            payload["entity_metadata"] = entity_metadata

        if channel_id is not MISSING:
            payload["channel_id"] = channel_id

        if image is not MISSING:
            payload["image"] = bytes_to_base64_data(image)

        return self.request(r, payload=payload)

    def delete_scheduled_event(self, guild_id: int, event_id: int):
        r = Route("DELETE", "/guilds/{guild_id}/scherduled-events/{event_id}", guild_id=guild_id, event_id=event_id)
        return self.request(r)

    def get_scheduled_event_users(
        self,
        guild_id: int,
        event_id: int,
        *,
        limit: int = 100,
        with_member: int = False,
        before: Optional[int] = None,
        after: Optional[int] = None
    ):
        r = Route("GET", "/guilds/{guild_id}/scheduled-events/{event_id}", guild_id=guild_id, event_id=event_id)
        params = {
            "limit": limit,
            "with_member": int(with_member),
        }

        if before is not None:
            params["before"] = before

        if after is not None:
            params["after"] = after

        return self.request(r, params=params)
