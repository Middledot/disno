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

from typing import Union, Literal


class AuthenticationlessWebhookEndpoints:  # TODO: naming?
    def get_webhook_with_token(self, webhook_id: int, webhook_token: str):
        r = Route("GET", "/webhooks/{webhook_id}/{webhook_token}", webhook_id=webhook_id, webhook_token=webhook_token)
        return self.request(r)

    def edit_webhook_with_token(
        self,
        webhook_id: int,
        webhook_token: str,
        *,
        name: str = MISSING,
        avatar: bytes = MISSING
    ):
        r = Route("PATCH", "/webhooks/{webhook_id}/{webhook_token}", webhook_id=webhook_id, webhook_token=webhook_token)
        payload = {}

        if name is not MISSING:
            payload["name"] = name

        if avatar is not MISSING:
            payload["avatar"] = bytes_to_base64_data(avatar)

        return self.request(r, payload=payload)

    def delete_webhook_with_token(self, webhook_id: int, webhook_token: str):
        r = Route("DELETE", "/webhooks/{webhook_id}/{webhook_token}", webhook_id=webhook_id, webhook_token=webhook_token)
        return self.request(r)

    def send_webhook_message(
        self,
        webhook_id: int,
        webhook_token: str,
        *,
        content: str = MISSING,
        username: str = MISSING,
        avatar_url: str = MISSING,
        tts: bool = MISSING,
        embeds = MISSING,
        allowed_mentions = MISSING,
        components = MISSING,
        files = None,
        flags = MISSING
    ):
        r = Route("DELETE", "/webhooks/{webhook_id}/{webhook_token}", webhook_id=webhook_id, webhook_token=webhook_token)
        payload = {"tts": int(tts)}

        if content is not MISSING:
            payload["content"] = content

        if username is not MISSING:
            payload["username"] = username

        if avatar_url is not MISSING:
            payload["avatar_url"] = avatar_url

        if embeds is not MISSING:
            payload["embeds"] = embeds

        if allowed_mentions is not MISSING:
            payload["allowed_mentions"] = allowed_mentions

        if components is not MISSING:
            payload["components"] = components

        if flags is not MISSING:
            payload["flags"] = flags

        if files is not None:
            form = self._prepare_form(payload, files)
            return self.request(r, data=form)
        else:
            return self.request(r, payload=payload)

    def get_webhook_message(
        self,
        webhook_id: int,
        webhook_token: str,
        message_id: Union[int, Literal["@original"]],
        *,
        thread_id: int
    ):
        r = Route("GET", "/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}", webhook_id=webhook_id, webhook_token=webhook_token, message_id=message_id)
        params = {"thread_id": thread_id}

        return self.request(r, params=params)

    def edit_webhook_message(
        self,
        webhook_id: int,
        webhook_token: str,
        message_id: Union[int, Literal["@original"]],
        *,
        content: str = MISSING,
        embeds = MISSING,
        allowed_mentions = MISSING,
        components = MISSING,
        files = None,
        thread_id: int = MISSING,
    ):
        r = Route("PATCH", "/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}", webhook_id=webhook_id, webhook_token=webhook_token, message_id=message_id)
        params = {"thread_id": thread_id}
        payload = {}

        if content is not MISSING:
            payload["content"] = content

        if embeds is not MISSING:
            payload["embeds"] = embeds

        if allowed_mentions is not MISSING:
            payload["allowed_mentions"] = allowed_mentions

        if components is not MISSING:
            payload["components"] = components

        if files is not None:
            form = self._prepare_form(payload, files)
            return self.request(r, data=form, params=params)
        else:
            return self.request(r, payload=payload, params=params)

    def delete_webhook_message(
        self,
        webhook_id: int,
        webhook_token: str,
        message_id: Union[int, Literal["@original"]],
        *,
        thread_id: int
    ):
        r = Route("DELETE", "/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}", webhook_id=webhook_id, webhook_token=webhook_token, message_id=message_id)
        params = {"thread_id": thread_id}
        return self.request(r, params=params)


class WebhookEndpoints(AuthenticationlessWebhookEndpoints):
    def create_webhook(
        self,
        channel_id: int,
        *,
        name: str,
        avatar: bytes = MISSING
    ):
        r = Route("POST", "/channels/{channel_id}/webhooks", channel_id=channel_id)
        payload = {"name": name}

        if avatar is not MISSING:
            payload["avatar"] = bytes_to_base64_data(avatar)

        return self.request(r, payload=payload)

    def get_guild_webhooks(
        self,
        guild_id: int,
    ):
        r = Route("POST", "/guilds/{guild_id}/webhooks", guild_id=guild_id)
        return self.request(r)

    def get_webhook(self, webhook_id: int):
        r = Route("GET", "/webhooks/{webhook_id}", webhook_id=webhook_id)
        return self.request(r)

    def edit_webhook(
        self,
        webhook_id: int,
        *,
        name: str = MISSING,
        avatar: bytes = MISSING,
        channel_id: int = MISSING,
        reason: str = None
    ):
        r = Route("PATCH", "/webhooks/{webhook_id}", webhook_id=webhook_id)
        payload = {}

        if name is not MISSING:
            payload["name"] = name

        if avatar is not MISSING:
            payload["avatar"] = bytes_to_base64_data(avatar)

        if channel_id is not MISSING:
            payload["channel_id"] = channel_id

        return self.request(r, payload=payload, reason=reason)

    def delete_webhook(self, webhook_id: int, *, reason = None):
        r = Route("DELETE", "/webhooks/{webhook_id}", webhook_id=webhook_id)
        return self.request(r, reason=reason)
