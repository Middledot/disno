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

from typing import Optional, List

class GuildEndpoints:
    def create_guild(
        self,
        *,
        name: str,
        icon: Optional[bytes] = None,
        verification_level: Optional[int] = None,
        default_message_notifications: Optional[int] = None,
        explicit_content_filter: Optional[int] = None,
        roles = None,
        channels = None,
        afk_channel_id: Optional[int] = None,
        afk_timeout: Optional[int] = None,
        system_channel_id: Optional[int] = None,
        system_channel_flags: Optional[int] = None,
    ):
        r = Route('POST', '/guilds')

        payload = {
            "name": str(name),
            "icon": bytes_to_base64_data(icon),
            "verification_level": verification_level,
            "default_message_notifications": default_message_notifications,
            "explicit_content_filter": explicit_content_filter,
            "roles": roles,
            "channels": channels,
            "afk_channel_id": afk_channel_id,
            "afk_timeout": afk_timeout,
            "system_channel_id": system_channel_id,
            "system_channel_flags": system_channel_flags,
        }

        return self.request(r, payload=payload)

    def get_guild(
        self,
        guild_id: int,
        *,
        with_counts: Optional[bool] = False
    ):
        r = Route('GET', '/guilds/{guild_id}', guild_id=guild_id)

        params = {
            "with_counts": int(with_counts),
        }

        return self.request(r, params=params)

    def get_guild_preview(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/preview", guild_id=guild_id)
        return self.request(r)

    def edit_guild(
        self,
        guild_id: int,
        *,
        name: str = MISSING,
        verification_level: int = MISSING,
        default_message_notifications: int = MISSING,
        explicit_content_filter: int = MISSING,
        afk_channel_id: int = MISSING,
        afk_timeout: int = MISSING,
        icon: bytes = MISSING,
        owner_id: int = MISSING,
        splash: bytes = MISSING,
        discovery_splash: bytes = MISSING,
        banner: bytes = MISSING,
        system_channel_id: int = MISSING,
        system_channel_flags: int = MISSING,
        rules_channel_id: int = MISSING,
        public_updates_channel_id: int = MISSING,
        preferred_locale: str = MISSING,
        features: str = MISSING,
        description: str = MISSING,
        premium_progress_bar_enabled: bool = MISSING
    ):
        r = Route("PATCH", "/guilds/{guild_id}", guild_id=guild_id)
        payload = {}

        if name is not MISSING:
            payload["name"] = name

        if verification_level is not MISSING:
            payload["verification_level"] = verification_level

        if default_message_notifications is not MISSING:
            payload["default_message_notifications"] = default_message_notifications

        if explicit_content_filter is not MISSING:
            payload["explicit_content_filter"] = explicit_content_filter

        if afk_channel_id is not MISSING:
            payload["afk_channel_id"] = afk_channel_id

        if afk_timeout is not MISSING:
            payload["afk_timeout"] = afk_timeout

        if icon is not MISSING:
            payload["icon"] = bytes_to_base64_data(icon)

        if owner_id is not MISSING:
            payload["owner_id"] = owner_id

        if splash is not MISSING:
            payload["splash"] = bytes_to_base64_data(splash)

        if discovery_splash is not MISSING:
            payload["discovery_splash"] = bytes_to_base64_data(discovery_splash)

        if banner is not MISSING:
            payload["banner"] = bytes_to_base64_data(banner)

        if system_channel_id is not MISSING:
            payload["system_channel_id"] = system_channel_id

        if system_channel_flags is not MISSING:
            payload["system_channel_flags"] = system_channel_flags

        if rules_channel_id is not MISSING:
            payload["rules_channel_id"] = rules_channel_id

        if public_updates_channel_id is not MISSING:
            payload["public_updates_channel_id"] = public_updates_channel_id

        if preferred_locale is not MISSING:
            payload["preferred_locale"] = preferred_locale

        if features is not MISSING:
            payload["features"] = features

        if description is not MISSING:
            payload["description"] = description

        if premium_progress_bar_enabled is not MISSING:
            payload["premium_progress_bar_enabled"] = premium_progress_bar_enabled

        return self.request(r, payload=payload)

    def delete_guild(self, guild_id: int):
        r = Route("DELETE", "/guilds/{guild_id}", guild_id=guild_id)
        return self.request(r)

    def get_member(self, guild_id: int, user_id: int):
        r = Route("GET", "/guilds/{guild_id}/members/{user_id}", guild_id=guild_id, user_id=user_id)
        return self.request(r)

    def list_members(self, guild_id: int, *, limit: int = None, after: int = None):
        r = Route("GET", "/guilds/{guild_id}/members", guild_id=guild_id)
        params = {}

        if limit is not None:
            params["limit"] = limit

        if after is not None:
            params["after"] = after

        return self.request(r, params=params)

    def search_members(self, guild_id: int, *, query: str, limit: int = None):
        r = Route("GET", "/guilds/{guild_id}/members/search", guild_id=guild_id)
        params = {"query": query}

        if limit is not None:
            params["limit"] = limit

        return self.request(r, params=params)

    def add_member(
        self,
        guild_id: int,
        user_id: int,
        *,
        access_token: str,
        nick: str = None,
        roles: List[int] = None,
        mute: bool = None,
        deaf: bool = None
    ):
        r = Route("PUT", "/guilds/{guild_id}/members/{user_id}", guild_id=guild_id, user_id=user_id)
        payload = {"access_token": access_token}

        if nick is not None:
            payload["nick"] = nick

        if roles is not None:
            payload["roles"] = roles

        if mute is not None:
            payload["mute"] = mute

        if deaf is not None:
            payload["deaf"] = deaf

        return self.request(r, payload=payload)

    def edit_member(
        self,
        guild_id: int,
        user_id: int,
        *,
        nick: str = MISSING,
        roles: List[int] = MISSING,
        mute: bool = MISSING,
        deaf: bool = MISSING,
        channel_id: int = MISSING,
        communication_disabled_until: str = MISSING
    ):
        r = Route("PATCH", "/guilds/{guild_id}/members/{user_id}", guild_id=guild_id, user_id=user_id)
        payload = {}

        if nick is not MISSING:
            payload["nick"] = nick

        if roles is not MISSING:
            payload["roles"] = roles

        if mute is not MISSING:
            payload["mute"] = mute
        
        if deaf is not MISSING:
            payload["deaf"] = deaf

        if channel_id is not MISSING:
            payload["channel_id"] = channel_id

        if communication_disabled_until is not MISSING:
            payload["communication_disabled_until"] = communication_disabled_until

        return self.request(r, payload=payload)

    def edit_current_member(self, guild_id: int, *, nick: str = MISSING, reason: str = None):
        r = Route("PATCH", "/guilds/{guild_id}/members/@me", guild_id=guild_id)
        payload = {}

        if nick is not MISSING:
            payload["nick"] = nick

        return self.request(r, payload=payload)

    def add_member_role(self, guild_id: int, user_id: int, role_id: int, *, reason: str = None):
        r = Route("PUT", "/guilds/{guild_id}/members/{user_id}/roles/{role_id}", guild_id=guild_id, user_id=user_id, role_id=role_id)
        return self.request(r, reason=reason)

    def add_member_role(self, guild_id: int, user_id: int, role_id: int, *, reason: str = None):
        r = Route("DELETE", "/guilds/{guild_id}/members/{user_id}/roles/{role_id}", guild_id=guild_id, user_id=user_id, role_id=role_id)
        return self.request(r, reason=reason)

    def kick_member(self, guild_id: int, user_id: int, *, reason: str = None):
        r = Route("DELETE", "/guilds/{guild_id}/members/{user_id}", guild_id=guild_id, user_id=user_id)
        return self.request(r, reason=reason)

    def ban_member(self, guild_id: int, user_id: int, *, delete_message_days: int = 0, reason: str = None):
        r = Route("PUT", "/guilds/{guild_id}/members/{user_id}", guild_id=guild_id, user_id=user_id)
        payload = {"delete_message_days": delete_message_days}

        return self.request(r, payload=payload, reason=reason)

    def unban_member(self, guild_id: int, user_id: int, *, reason: str = None):
        r = Route("DELETE", "/guilds/{guild_id}/members/{user_id}", guild_id=guild_id, user_id=user_id)
        return self.request(r, reason=reason)

    def get_guild_bans(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/bans", guild_id=guild_id)
        return self.request(r)

    def get_guild_ban(self, guild_id: int, user_id: int):
        r = Route("GET", "/guilds/{guild_id}/bans", guild_id=guild_id, user_id=user_id)
        return self.request(r)

    def get_roles(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/roles", guild_id=guild_id)
        return self.request(r)

    def create_roles(
        self,
        guild_id: int,
        *,
        name: str = None,
        permissions: str = None,
        color: int = None,
        hoist: bool = None,
        icon: bytes = None,
        unicode_emoji: str = None,
        mentionable: bool = None,
        reason: str = None
    ):
        r = Route("POST", "/guilds/{guild_id}/roles", guild_id=guild_id)
        payload = {}

        if name is not None:
            payload["name"] = name

        if permissions is not None:
            payload["permissions"] = permissions

        if color is not None:
            payload["color"] = color

        if hoist is not None:
            payload["hoist"] = int(hoist)

        if icon is not None:
            payload["icon"] = bytes_to_base64_data(icon)

        if unicode_emoji is not None:
            payload["unicode_emoji"] = unicode_emoji

        if mentionable is not None:
            payload["mentionable"] = int(mentionable)

        return self.request(r, reason=reason)

    def edit_role_position(self, guild_id: int, *, role_id: int, position: int = MISSING, reason: str = None):
        r = Route("PATCH", "/guilds/{guild_id}/roles", guild_id=guild_id)
        payload = {"id": role_id}

        if position is not MISSING:
            payload["position"] = position

        return self.request(r, payload=payload, reason=reason)

    def edit_role(
        self,
        guild_id: int,
        role_id: int,
        *,
        name: str = MISSING,
        permissions: str = MISSING,
        color: int = MISSING,
        hoist: bool = MISSING,
        icon: bytes = MISSING,
        unicode_emoji: str = MISSING,
        mentionable: bool = MISSING,
        reason: str = None
    ):
        r = Route("PATCH", "/guilds/{guild_id}/roles/{role_id}", guild_id=guild_id, role_id=role_id)
        payload = {}

        if name is not MISSING:
            payload["name"] = name

        if permissions is not MISSING:
            payload["permissions"] = permissions

        if color is not MISSING:
            payload["color"] = color

        if hoist is not MISSING:
            payload["hoist"] = hoist

        if icon is not MISSING:
            payload["icon"] = icon

        if unicode_emoji is not MISSING:
            payload["unicode_emoji"] = unicode_emoji

        if mentionable is not MISSING:
            payload["mentionable"] = mentionable

        return self.request(r, payload=payload, reason=reason)

    def delete_role(self, guild_id: int, role_id: int, *, reason: str = None):
        r = Route("DELETE", "/guilds/{guild_id}/roles/{role_id}", guild_id=guild_id, role_id=role_id)
        return self.request(r, reason=reason)

    def get_prune_count(self, guild_id: int, *, days: int = None, include_roles: List[int] = None):
        r = Route("GET", "/guilds/{guild_id}/prune", guild_id=guild_id)
        params = {}

        if days is not None:
            params["days"] = days

        if include_roles is not None:
            params["include_roles"] = ",".join(str(role) for role in include_roles)

        return self.request(r, params=params)

    def begin_prune(
        self,
        guild_id: int,
        *,
        days: int = None,
        compute_prune_count: bool = True,
        include_roles: List[int] = None,
        reason: str = None
    ):
        r = Route("GET", "/guilds/{guild_id}/prune", guild_id=guild_id)
        payload = {}

        if days is not None:
            payload["days"] = days

        if compute_prune_count is not True:
            payload["compute_prune_count"] = compute_prune_count

        if include_roles is not None:
            payload["include_roles"] = include_roles

        return self.request(r, params=payload, reason=reason)

    def get_integrations(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/integrations", guild_id=guild_id)
        return self.request(r)

    def delete_integrations(self, guild_id: int, integration_id: int, *, reason: str = None):
        r = Route("DELETE", "/guilds/{guild_id}/integrations/{integration_id}", guild_id=guild_id, integration_id=integration_id)
        return self.request(r, reason=reason)

    def get_widget_settings(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/widget", guild_id=guild_id)
        return self.request(r)

    def get_widget(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/widget.json", guild_id=guild_id)
        return self.request(r)

    def edit_widget(
        self,
        guild_id: int,
        *,
        enabled: bool = MISSING,
        channel_id: int = MISSING,
        reason: str = None
    ):
        r = Route("PATCH", "/guilds/{guild_id}/widget", guild_id=guild_id)
        payload = {}

        if enabled is not MISSING:
            payload["enabled"] = enabled

        if channel_id is not MISSING:
            payload["channel_id"] = channel_id

        return self.request(r, reason=reason)

    # https://discord.com/developers/docs/resources/guild#get-guild-widget-image

    def get_welcome_screen(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/welcome-screen", guild_id=guild_id)
        return self.request(r)

    def edit_welcome_screen(
        self,
        guild_id: int,
        *,
        enabled: bool = MISSING,
        welcome_channels = MISSING,
        description: str = MISSING
    ):
        r = Route("GET", "/guilds/{guild_id}/welcome-screen", guild_id=guild_id)
        payload = {}

        if enabled is not MISSING:
            payload["enabled"] = enabled

        if welcome_channels is not MISSING:
            payload["welcome_channels"] = welcome_channels

        if description is not MISSING:
            payload["description"] = description

        return self.request(r)

    def get_guild_audit_logs(
        self,
        guild_id: int,
        *,
        user_id: int = MISSING,
        action_type: int = MISSING,
        before: int = MISSING,
        limit: int = 50,
    ):
        r = Route("GET", "/guilds/{guild_id}/audit-logs", guild_id=guild_id)
        params = {"limit": limit}

        if user_id is not MISSING:
            params["user_id"] = user_id

        if action_type is not MISSING:
            params["action_type"] = action_type

        if before is not MISSING:
            params["before"] = before

        return self.request(r, params=params)

    def get_guild_emojis(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/emojis", guild_id=guild_id)
        return self.request(r)

    def get_guild_emoji(self, guild_id: int, emoji_id: int):
        r = Route("GET", "/guilds/{guild_id}/emojis/{emoji_id}", guild_id=guild_id, emoji_id=emoji_id)
        return self.request(r)

    def create_guild_emoji(
        self,
        guild_id: int,
        *,
        name: str,
        image: bytes,
        roles = MISSING,
        reason: str = None
    ):
        r = Route("POST", "/guilds/{guild_id}/emojis", guild_id=guild_id)
        payload = {
            "name": name,
            "image": image,
        }

        if roles is not MISSING:
            payload["roles"] = roles

        return self.request(r, payload=payload, reason=reason)

    def edit_guild_emoji(
        self,
        guild_id: int,
        emoji_id: int,
        *,
        name: str = MISSING,
        roles = MISSING,
        reason: str = None
    ):
        r = Route("PATCH", "/guilds/{guild_id}/emojis/{emoji_id}", guild_id=guild_id, emoji_id=emoji_id)
        payload = {}

        if name is not MISSING:
            payload["name"] = name
        
        if roles is not MISSING:
            payload["roles"] = roles
        
        return self.request(r, payload=payload, reason=reason)

    def delete_guild_emoji(self, guild_id: int, emoji_id: int, *, reason: str = None):
        r = Route("DELETE", "/guilds/{guild_id}/emojis/{emoji_id}", guild_id=guild_id, emoji_id=emoji_id)
        return self.request(r, reason=reason)
