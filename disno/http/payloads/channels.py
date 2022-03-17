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

from typing import List, Literal, TypedDict

ChannelType = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


class PermissionOverwrite(TypedDict):
    id: int
    type: Literal[0, 1]
    allow: str
    deny: str


class _BaseChannel(TypedDict):
    id: int
    type: ChannelType
    name: str
    #last_message_id: int


class GuildChannel(_BaseChannel):
    type: Literal[1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    guild_id: int
    position: int
    permission_overwrites: List
    name: str


class TextChannel(GuildChannel):
    type: Literal[0]
    topic: str
    nsfw: bool
    rate_limit_per_user: int


class VocalChannel(GuildChannel):
    bitrate: int
