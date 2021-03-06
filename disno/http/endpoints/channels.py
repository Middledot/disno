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

from typing import List, Optional

from ..route import Route
from ..enums import AuthType
from .. import utils

MISSING = utils.MISSING

class ChannelEndpoints:
    # Channels and Threads (and Group Channels technically)
    # https://discord.com/developers/docs/resources/channel

    def get_channel(
        self,
        channel_id: int
    ):
        r = Route('GET', '/channels/{channel_id}', channel_id=channel_id)
        return self.request(r)

    def get_guild_channels(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/channels", guild_id=guild_id)
        return self.request(r)

    def create_channel(
        self,
        guild_id: int,
        *,
        name: str,
        type: Optional[int] = None,
        topic: Optional[str] = None,
        bitrate: Optional[int] = None,
        user_limit: Optional[int] = None,
        rate_limit_per_user: Optional[int] = None,
        position: Optional[int] = None,
        permission_overwrites = None,
        parent_id: Optional[int] = None,
        nsfw: Optional[bool] = None,
        reason: str = None
    ):
        r = Route("POST", "/guilds/{guild_id}/channels", guild_id=guild_id)
        payload = {
            "name": name,
            "type": type,
            "topic": topic,
            "bitrate": bitrate,
            "user_limit": user_limit,
            "rate_limit_per_user": rate_limit_per_user,
            "position": position,
            "permission_overwrites": permission_overwrites,
            "parent_id": parent_id,
            "nsfw": int(nsfw)
        }

        return self.request(r, payload=payload, reason=reason)

    def edit_channel_position(self, guild_id: int, *, channel_id: int, position: int = None, lock_permissions: bool = None, parent_id: int = None, reason: str = None):
        r = Route("PATCH", "/guilds/{guild_id}/channels", guild_id=guild_id)
        payload = {
            "id": channel_id,
        }

        if position is not None:
            payload["position"] = position
        
        if lock_permissions is not None:
            payload["lock_permissions"] = lock_permissions
        
        if parent_id is not None:
            payload["parent_id"] = parent_id

        return self.request(r, payload=payload, reason=reason)

    def create_dm_from_current_user(self, token, *, recipient_id):
        r = Route('POST', '/users/@me/channels')
        payload = {"recipient_id": recipient_id}

        return self.request(r, payload=payload, auth=AuthType.bearer, token=token)

    def create_group_from_current_user(self, token, *, access_tokens, nicks):
        r = Route('POST', '/users/@me/channels')
        payload = {
            "access_tokens": access_tokens,
            "nicks": nicks,
        }

        return self.request(r, payload=payload, auth=AuthType.bearer, token=token)

    def add_group_recipient(self, channel_id: int, user_id: int, *, access_token: str = None, nick: str = None):
        r = Route('PUT', '/channels/{channel_id}/recipients/{user_id}', channel_id=channel_id, user_id=user_id)
        payload = {
            "access_token": access_token,
            "nick": nick
        }

        return self.request(r, payload=payload)

    def remove_group_recipient(self, channel_id: int, user_id: int):
        r = Route('DELETE', '/channels/{channel_id}/recipients/{user_id}', channel_id=channel_id, user_id=user_id)
        return self.request(r)

    def edit_group_channel(
        self,
        channel_id,
        *,
        name: str = MISSING,
        icon: bytes = MISSING
    ):
        r = Route('PATCH', '/channels/{channel_id}', channel_id=channel_id)
        payload = {}

        if name is not MISSING:
            payload["name"] = name

        if icon is not MISSING:
            payload["icon"] = utils.bytes_to_base64_data(icon)

        return self.request(r, payload=payload)

    def edit_guild_channel(
        self,
        channel_id,
        *,
        name: str = MISSING,
        type: int = MISSING,
        position: int = MISSING,
        topic: str = MISSING,
        nsfw: bool = MISSING,
        rate_limit_per_user: int = MISSING,
        bitrate: int = MISSING,
        user_limit: int = MISSING,
        permissions_overwrites: List = MISSING,
        parent_id: int = MISSING,
        rtc_region: str = MISSING,
        video_quality_mode: int = MISSING,
        default_auto_archive_duration: int = MISSING,
        reason: str = None
    ):
        r = Route('PATCH', '/channels/{channel_id}', channel_id=channel_id)
        payload = {}

        if name is not MISSING:
            payload["name"] = name

        if type is not MISSING:
            payload["type"] = type

        if position is not MISSING:
            payload["position"] = position

        if topic is not MISSING:
            payload["topic"] = topic

        if nsfw is not MISSING:
            payload["nsfw"] = int(nsfw)

        if rate_limit_per_user is not MISSING:
            payload["rate_limit_per_user"] = rate_limit_per_user

        if bitrate is not MISSING:
            payload["bitrate"] = bitrate

        if user_limit is not MISSING:
            payload["user_limit"] = user_limit

        if permissions_overwrites is not MISSING:
            payload["permissions_overwrites"] = permissions_overwrites

        if parent_id is not MISSING:
            payload["parent_id"] = parent_id

        if rtc_region is not MISSING:
            payload["rtc_region"] = rtc_region

        if video_quality_mode is not MISSING:
            payload["video_quality_mode"] = video_quality_mode

        if default_auto_archive_duration is not MISSING:
            payload["default_auto_archive_duration"] = default_auto_archive_duration

        return self.request(r, payload=payload, reason=reason)

    def edit_thread(
        self,
        channel_id,
        *,
        name: str = MISSING,
        archived: bool = MISSING,
        auto_archive_duration: int = MISSING,
        locked: bool = MISSING,
        invitable: bool = MISSING,
        rate_limit_per_user: int = MISSING,
        reason: str = MISSING
    ):
        r = Route('PATCH', '/channels/{channel_id}', channel_id=channel_id)
        payload = {}

        if name is not MISSING:
            payload["name"] = name

        if archived is not MISSING:
            payload["archived"] = int(archived)

        if auto_archive_duration is not MISSING:
            payload["auto_archived_duration"] = auto_archive_duration

        if locked is not MISSING:
            payload["locked"] = locked

        if invitable is not MISSING:
            payload["invitable"] = invitable

        if rate_limit_per_user is not MISSING:
            payload["rate_limit_per_user"] = rate_limit_per_user

        return self.request(r, payload=payload, reason=reason)

    def delete_channel(self, channel_id: int, *, reason: str = None):
        r = Route('DELETE', '/channels/{channel_id}', channel_id=channel_id)
        return self.request(r, reason=reason)

    def edit_channel_overwrite(
        self,
        channel_id: int,
        overwrite_id: int,
        *,
        allow: str = None,
        deny: str = None,
        type: int = None,
        reason: str = None
    ):
        r = Route('PUT', '/channels/{channel_id}/permissions/{overwrite_id}', channel_id=channel_id, overwrite_id=overwrite_id)
        payload = {
            "allow": allow,
            "deny": deny,
            "type": type,
        }

        return self.request(r, payload=payload, reason=reason)

    def delete_channel_overwrite(self, channel_id: int, overwrite_id: int, *, reason: str = None):
        r = Route('DELETE', '/channels/{channel_id}/permissions/{overwrite_id}', channel_id=channel_id, overwrite_id=overwrite_id)
        return self.request(r, reason=reason)

    def follow_news_channel(self, channel_id: int, *, webhook_channel_id: int = None):
        r = Route('POST', '/channels/{channel_id}/', channel_id=channel_id)
        payload = {}

        if webhook_channel_id is not None:
            payload["webhook_channel_id"] = webhook_channel_id

        return self.request(r, payload=payload)

    def start_typing(self, channel_id: int):
        r = Route('POST', '/channels/{channel_id}/typing', channel_id=channel_id)
        return self.request(r)

    def get_pinned_messages(self, channel_id: int):
        r = Route('GET', '/channels/{channel_id}/pins', channel_id=channel_id)
        return self.request(r)

    def pin_message(self, channel_id: int, message_id: int, *, reason: str = None):
        r = Route('PUT', '/channels/{channel_id}/pins/{message_id}', channel_id=channel_id, message_id=message_id)
        return self.request(r, reason=reason)

    def unpin_message(self, channel_id: int, message_id: int, *, reason: str = None):
        r = Route('DELETE', '/channels/{channel_id}/pins/{message_id}', channel_id=channel_id, message_id=message_id)
        return self.request(r, reason=reason)

    def start_thread_with_message(
        self,
        channel_id: int,
        message_id: int,
        *,
        name: str,
        auto_archive_duration: int = None,
        rate_limit_per_user: int = None,
        reason: str = None
    ):
        r = Route('POST', '/channels/{channel_id}/messages/{message_id}/threads', channel_id=channel_id, message_id=message_id)
        payload = {
            "name": name
        }

        if auto_archive_duration is not None:
            payload["auto_archive_duration"] = auto_archive_duration

        if rate_limit_per_user is not None:
            payload["rate_limit_per_user"] = rate_limit_per_user

        return self.request(r, payload=payload, reason=reason)

    def start_thread_without_message(
        self,
        channel_id: int,
        *,
        name: str,
        auto_archive_duration: int = None,
        type: int = None,
        invitable: int = None,
        rate_limit_per_user: int = None,
        reason: str = None
    ):
        r = Route('POST', '/channels/{channel_id}/threads', channel_id=channel_id)
        payload = {
            "name": name
        }

        if auto_archive_duration is not None:
            payload["auto_archive_duration"] = auto_archive_duration
        
        if type is not None:
            payload["type"] = type
        
        if invitable is not None:
            payload["invitable"] = invitable

        if rate_limit_per_user is not None:
            payload["rate_limit_per_user"] = rate_limit_per_user

        return self.request(r, payload=payload, reason=reason)

    def join_thread(self, thread_id: int):
        r = Route('PUT', '/channels/{thread_id}/thread-members/@me', thread_id=thread_id)
        return self.request(r)

    def leave_thread(self, thread_id: int):
        r = Route('DELETE', '/channels/{thread_id}/thread-members/@me', thread_id=thread_id)
        return self.request(r)

    def add_thread_member(self, thread_id: int, user_id: int):
        r = Route('PUT', '/channels/{thread_id}/thread-members/{user_id}', thread_id=thread_id, user_id=user_id)
        return self.request(r)

    def remove_thread_member(self, thread_id: int, user_id: int):
        r = Route('DELETE', '/channels/{thread_id}/thread-members/{user_id}', thread_id=thread_id, user_id=user_id)
        return self.request(r)

    def get_thread_member(self, thread_id: int, user_id: int):
        r = Route('GET', '/channels/{thread_id}/thread-members/{user_id}', thread_id=thread_id, user_id=user_id)
        return self.request(r)

    def list_active_threads(self, channel_id: int):
        r = Route('GET', '/channels/{channel_id}/threads/active', channel_id=channel_id)
        return self.request(r)

    def list_active_guild_threads(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/threads/active", guild_id=guild_id)
        return self.request(r)

    def get_public_archived_threads(self, channel_id: int, *, limit: int = None, before: int = None):
        r = Route('GET', '/channels/{channel_id}/threads/archived/public', channel_id=channel_id)
        params = {}

        if limit is not None:
            params["limit"] = limit

        if before is not None:
            params["before"] = before

        return self.request(r, params=params)

    def get_private_archived_threads(self, channel_id: int, *, limit: int = None, before: int = None):
        r = Route('GET', '/channels/{channel_id}/threads/archived/private', channel_id=channel_id)
        params = {}

        if limit is not None:
            params["limit"] = limit

        if before is not None:
            params["before"] = before

        return self.request(r, params=params)

    def get_joined_private_archived_threads(self, channel_id: int, *, limit: int = None, before: int = None):
        r = Route('GET', '/channels/{channel_id}/users/@me/threads/archived/private', channel_id=channel_id)
        params = {}

        if limit is not None:
            params["limit"] = limit

        if before is not None:
            params["before"] = before

        return self.request(r, params=params)
