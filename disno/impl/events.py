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

from lib2to3.pgen2 import token
import aiohttp
import asyncio
import sys

from ..websockets import Websocket
from ..http import HTTPClient

class GatewayClient:
    def __init__(self, loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        user_agent = 'DiscordBot (https://github.com/QwireTeam/disno {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format("0.0.1", sys.version_info, aiohttp.__version__)

        self.http = HTTPClient(loop=self.loop)
        self.ws = None
        self.listeners = {}

    @property
    def session(self):
        return self.http.session

    async def login(self):
        data = await self.http.get_current_user()
        print(data)

    async def connect(self):
        ws_params = {
            'initial': True,
            'shard_id': None,
        }
        self.ws = await Websocket.initialize(processor=self.process_events, token=self.http.bot_token)
        while True:
            await self.ws.poll_receive()

    def listener(self, event = None):
        def inner(func):
            name = event or func.__name__
            if name not in self.listeners:
                self.listeners[name] = [func]
            else:
                self.listeners[name].append(func)
            return func
        return inner

    async def process_events(self, event, data):
        if event.lower() in self.listeners:
            for l in self.listeners[event.lower()]:
                await l(data)

    async def start(self):
        await self.login()
        await self.connect()
    
    def run(self, token):
        self.http.bot_token = token

        async def runner():
            await self.start()

        future = asyncio.ensure_future(runner(), loop=self.loop)
        self.loop.run_forever()
