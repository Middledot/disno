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

import asyncio
import aiohttp
import sys
from typing import Dict

from . import utils
from .enums import AuthType
from .route import Route
from .endpoints import *

endpoints = (
    GuildEndpoints,
    UserEndpoints,
    OAuth2Endpoints,
    ChannelEndpoints,
    MessageEndpoints,
    ReactionEndpoints,
    ApplicationCommandEndpoints,
    InteractionEndpoints,
    WebhookEndpoints,
    ScheduledEventEndpoints,
    TemplateEndpoints,
)

class AutoUnlocker:
    def __init__(self, lock):
        self.lock = lock

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback
    ) -> None:
        if self.lock.locked():
            self.lock.release()

class Requester:
    def __init__(self, session: aiohttp.ClientSession, client_id: str = None, client_secret: str = None, bot_token: str = None):
        self.client_id: int = client_id
        self.client_secret: str = client_secret
        self.bot_token: str = bot_token
        self.ratelimit_locks: Dict[str, asyncio.Lock] = {}
        self.buckets: Dict[str, Route] = {}
        self.global_lock: asyncio.Event = asyncio.Event()
        self.global_lock.set()

        user_agent = 'DiscordBot (https://github.com/QwireDev/disno {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent: str = user_agent.format("1.0.0a1", sys.version_info, aiohttp.__version__)

        self.session: aiohttp.ClientSession = session

    def _prepare_form(self, payload, files):
        form = []
        attachments = []

        for index, file in enumerate(files):
            attachments.append(
                {
                    'id': index,
                    'filename': file['filename'],
                    'description': "a meme"
                }
            )
            form.append(
                {
                    'name': 'files[%s]' % index,
                    'value': file['fp'],
                    'filename': file['filename'],
                    'content_type': 'application/octet-stream'
                }
            )
        payload['attachments'] = attachments
        form_data = aiohttp.FormData(quote_fields=False)
        form_data.add_field('payload_json', utils.to_json(payload))
        for f in form:
            form_data.add_field(
                f['name'],
                f['value'],
                filename=f['filename'],
                content_type=f['content_type']
            )
        return form_data

    async def request(
        self,
        route,
        payload = None,
        params = None,
        data = None,
        reason = None,
        auth = AuthType.bot,
        token = None,
    ):
        to_pass = {}
        method = route.method
        url = route.url
        bucket = self.buckets.get(route.bucket) or route.bucket

        lock = self.ratelimit_locks.get(bucket, None)
        if lock is None:
            lock = asyncio.Lock()
            self.ratelimit_locks[bucket] = lock

        headers = {
            "User-Agent": self.user_agent
        }

        if self.bot_token is not None and auth is AuthType.bot:
            headers["Authorization"] = "Bot " + self.bot_token
        elif token is not None and auth is AuthType.bearer:
            headers["Authorization"] = "Bearer " + token

        if reason is not None:
            headers["X-Audit-Log-Reason"] = utils.uriquote(reason)

        if data:
            to_pass["data"] = data
        elif payload is not None:
            headers["Content-Type"] = "application/json"
            to_pass["data"] = utils.to_json(payload)
        else:
            headers["Content-Type"] = "application/json"

        if params:
            to_pass["params"] = params

        to_pass["headers"] = headers

        if not self.global_lock.is_set():
            await self.global_lock.wait()

        await lock.acquire()
        with AutoUnlocker(lock):
            for tries in range(5):
                async with self.session.request(method, url, **to_pass) as res:
                    data = await res.json()

                    new_bucket = res.headers.get('x-ratelimit-bucket', None)
                    if new_bucket and new_bucket != bucket:
                        route._bucket = new_bucket
                        self.buckets[bucket] = new_bucket
                        if self.ratelimit_locks.get(bucket, None) is not None:
                            self.ratelimit_locks.pop(bucket)
                            self.ratelimit_locks[new_bucket] = lock

                    remaining = res.headers.get("x-ratelimit-limit", None)
                    if remaining == '0' and res.status != 429:
                        delay = res.headers.get("x-ratelimit-reset-after")
                        self.loop.call_later(delay, lock.release)

                    if 300 > res.status >= 200:
                        return data

                    if res.status == 429:
                        if "via" not in res.headers:
                            raise
                        reset_after = res.headers.get("x-ratelimit-reset-after")
                        is_global = data.get("global", False)

                        if is_global:
                            self.global_lock.clear()

                        await asyncio.sleep(float(reset_after))

                        if is_global:
                            self.global_lock.set()

                    return data


class WebhookClient(Requester, AuthenticationlessWebhookEndpoints):
    def __init__(self, *, loop=None, session=None):
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

        self.loop = loop

        if session is None:
            session = aiohttp.ClientSession(loop=self.loop)

        super().__init__(session, client_id=None, client_secret=None, bot_token=None)

    async def request(
        self,
        route,
        payload = None,
        params = None,
        data = None,
        reason = None,
        auth = AuthType.none,
        token = None,
    ):
        return await super().request(route, payload, params, data, reason, auth, token)


class InteractionsClient(Requester, WebhookEndpoints, InteractionEndpoints):
    def __init__(self, bot_token, *, loop=None, session=None):
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

        self.loop = loop

        if session is None:
            session = aiohttp.ClientSession(loop=self.loop)

        super().__init__(session, client_id=None, client_secret=None, bot_token=bot_token)


class HTTPClient(Requester, *endpoints):
    def __init__(self, bot_token = None, client_id = None, client_secret = None, *, loop=None, session=None):
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

        self.loop = loop

        if session is None:
            session = aiohttp.ClientSession(loop=self.loop)

        super().__init__(session, client_id=client_id, client_secret=client_secret, bot_token=bot_token)

    async def get_gateway(self, *, encoding: str = 'json', zlib: bool = True) -> str:
        data = await self.client.session.request("GET", "https://discord.com/api/v9/gateway")
        if zlib:
            value = '{0}?encoding={1}&v=9&compress=zlib-stream'
        value = '{0}?encoding={1}&v=9'
        return value.format((await data.json())['url'], encoding)
