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


class InteractionEndpoints:
    def create_interaction_response(
        self,
        interaction_id: int,
        interaction_token: str,
        *,
        type: int,
        data
    ):
        r = Route("POST", "/interactions/{interaction_id}/{interaction_token}/callback", interaction_id=interaction_id, interaction_token=interaction_token)
        payload = {
            "type": type,
            "data": data
        }
        return self.request(r, payload=payload)

    def get_original_interaction_response(self, application_id: int, interaction_token: str):
        return self.get_webhook_message(webhook_id=application_id, webhook_token=interaction_token, message_id="@original")

    def edit_original_interaction_response(
        self,
        application_id: int,
        interaction_token: str,
        *,
        content: str = MISSING,
        embeds = MISSING,
        allowed_mentions = MISSING,
        components = MISSING,
        files = None,
        thread_id: int = MISSING,
    ):
        payload = {}

        if content is not MISSING:
            payload["content"] = content

        if embeds is not MISSING:
            payload["embeds"] = embeds

        if allowed_mentions is not MISSING:
            payload["allowed_mentions"] = allowed_mentions

        if components is not MISSING:
            payload["components"] = components

        if files is not MISSING:
            payload["files"] = files

        if thread_id is not MISSING:
            payload["thread_id"] = thread_id

        return self.edit_webhook_message(
            webhook_id=application_id,
            webhook_token=interaction_token,
            message_id="@original",
            **payload
        )

    def delete_original_interaction_response(self, application_id: int, interaction_token: str):
        return self.delete_webhook_message(webhook_id=application_id, webhook_token=interaction_token, message_id="@original")

    def send_followup_message(
        self,
        application_id: int,
        interaction_token: str,
        *,
        content: str = MISSING,
        tts: bool = MISSING,
        embeds = MISSING,
        allowed_mentions = MISSING,
        components = MISSING,
        files = None,
        ephemeral: bool = False
    ):
        payload = {"tts": int(tts)}

        if content is not MISSING:
            payload["content"] = content

        if embeds is not MISSING:
            payload["embeds"] = embeds

        if allowed_mentions is not MISSING:
            payload["allowed_mentions"] = allowed_mentions

        if components is not MISSING:
            payload["components"] = components

        if ephemeral is not False:
            payload["flags"] = 64

        if files is not None:
            payload["files"] = files

        return self.send_webhook_message(
            webhook_id=application_id,
            webhook_token=interaction_token,
            message_id="@original",
            **payload
        )

    def get_followup_message(self, application_id: int, interaction_token: str, message_id: int):
        return self.send_webhook_message(webhook_id=application_id, webhook_token=interaction_token, message_id=message_id)

    def edit_followup_message(
        self,
        application_id: int,
        interaction_token: str,
        message_id: int,
        *,
        content: str = MISSING,
        embeds = MISSING,
        allowed_mentions = MISSING,
        components = MISSING,
        files = None,
        thread_id: int = MISSING,
    ):
        payload = {}

        if content is not MISSING:
            payload["content"] = content

        if embeds is not MISSING:
            payload["embeds"] = embeds

        if allowed_mentions is not MISSING:
            payload["allowed_mentions"] = allowed_mentions

        if components is not MISSING:
            payload["components"] = components

        if files is not MISSING:
            payload["files"] = files

        if thread_id is not MISSING:
            payload["thread_id"] = thread_id

        return self.edit_webhook_message(
            webhook_id=application_id,
            webhook_token=interaction_token,
            message_id=message_id,
            **payload
        )

    def delete_followup_message(self, application_id: int, interaction_token: str, message_id: int):
        return self.delete_webhook_message(webhook_id=application_id, webhook_token=interaction_token, message_id=message_id)
