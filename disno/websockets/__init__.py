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
import threading
import zlib
import sys
import aiohttp

from .utils import to_json, from_json


class OPType:
    dispatch = 0
    heartbeat = 1
    identify = 2
    reconnect = 7
    hello = 10
    heartbeat_ack = 11


class Heartbeat(threading.Thread):
    def __init__(self, **kwargs):
        self.ws = kwargs.pop("ws")
        self.interval = kwargs.pop("interval")
        self.ev = threading.Event()

        super().__init__(**kwargs)
    
    def run(self):
        while not self.ev.wait(self.interval):
            data = self.get_payload()

            f = asyncio.run_coroutine_threadsafe(self.ws.send_json(data), loop=self.ws.loop)
            total = 10
            while True:
                try:
                    f.result(10)
                    break
                except:
                    total += 10
    
    def get_payload(self):
        return {
            "op": OPType.heartbeat,
            "d": self.ws.sequence
        }

    def stop(self):
        self.ev.set()


class BaseWebsocket:
    def __init__(self, bot_token: str, *, session: aiohttp.ClientSession = None, loop = None):
        user_agent = 'DiscordBot (https://github.com/QwireDev/disno {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format("1.0.0a.1", sys.version_info, aiohttp.__version__)
        self.token = bot_token

        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

        self.loop = loop

        if session is None:
            session = aiohttp.ClientSession(loop=self.loop)
        self.session = session

        self.socket = None
        self.heart = None
        self.sequence = None
        self.session_id = None

        self.thread_id = threading.get_ident()

        self._buffer = bytearray()
        self._inflator = zlib.decompressobj()

    async def send(self, data):
        await self.socket.send_str(data)

    async def send_json(self, data):
        print("[SENT]     ", data)
        await self.socket.send_str(to_json(data))

    async def ack_hello(self, data):
        self.heartbeat = Heartbeat(ws=self, interval=data["d"]["heartbeat_interval"] / 1000)
        await self.send_json(self.heartbeat.get_payload())
        self.heartbeat.start()

    async def identify_payload(self):
        package = {
            "op": OPType.identify,
            "d": {
                "token": self.token,
                "intents": 14079,
                "properties": {
                    "$os": "windows",
                    "$browser": "disno",
                    "$device": "disno"
                },
                "presence": {
                    "status": "online",
                    "activity": {'flags': 0, 'type': 0, 'name': "doon't ping", 'buttons': []},
                    "since": 0,
                    "afk": False
                }
            }
        }

        await self.send_json(package)

    async def resume_payload(self):
        resume_payload = {
            "op": 6,
            "d": {
                "token": self.token,
                "session_id": self.session_id,
                "seq": self.sequence
            }
        }

        await self.send_json(resume_payload)

    async def connect(self):
        kwargs = {
            'max_msg_size': 0,
            'timeout': 30.0,
            'autoclose': False,
            'headers': {
                'User-Agent': self.user_agent,
            }
        }

        return await self.session.ws_connect(self.gateway, **kwargs)

    async def process_receive(self, msg):
        try:
            data = from_json(msg)
        except:
            print(type(msg))
            print(msg)
        if data["s"] is not None:
            self.sequence = data["s"]
        op = data["op"]
        event = data["t"]
        print("[RECEIVED] ", data)
        if op == OPType.hello:
            await self.ack_hello(data)
        elif op == OPType.heartbeat:
            await self.send_json(self.heartbeat.get_payload())
        elif op == OPType.dispatch and event == 'READY':
            payload = data.get('d')
            self.session_id = payload.get('session_id')

        return op, event

    async def poll_receive(self):
        msg = await self.socket.receive(timeout=120)
        if type(msg.data) is bytes:
            self._buffer.extend(msg.data)

            # check if the last four bytes are equal to ZLIB_SUFFIX
            if len(msg.data) < 4 or msg.data[-4:] != b'\x00\x00\xff\xff':
                return

            # if the message *does* end with ZLIB_SUFFIX,
            # get the full message by decompressing the buffers
            # NOTE: the message is utf-8 encoded.
            msg = self._inflator.decompress(self._buffer)
            self._buffer = bytearray()
        await self.process_receive(msg)


class Websocket:
    def __init__(self, bot_token: str, *, session: aiohttp.ClientSession = None, loop = None):
        super().__init__(bot_token, session=session, loop=loop)

    @classmethod
    async def initialize(cls, *args, **kwargs):
        ws = cls(*args, **kwargs)

        ws.gateway = "wss://gateway.discord.gg?encoding='json'&v=9&compress=zlib-stream" # TODO: uhh
        ws.socket = await ws.connect()

        await ws.poll_receive()
        await ws.identify_payload()

        return ws

    async def process_receive(self, msg):
        try:
            data = from_json(msg)
        except:
            print(type(msg))
            print(msg)

        if data["s"] is not None:
            self.sequence = data["s"]

        op = data["op"]
        event = data["t"]
        print("[RECEIVED] ", data)
        if op == OPType.hello:
            await self.ack_hello(data)
        elif op == OPType.heartbeat:
            await self.send_json(self.heartbeat.get_payload())
        elif op == OPType.dispatch and event == 'READY':
            payload = data.get('d')
            self.session_id = payload.get('session_id')

        if op == OPType.reconnect:
            # TODO: Test if this works, I haven't gotten a reconnect yet
            self.heart.stop()
            await self.socket.close()
            self.socket = await self.connect()
            await self.resume_payload()
            self.heart = Heartbeat(ws=self, interval=self.heart.interval)
