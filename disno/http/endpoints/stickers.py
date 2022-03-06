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


class StickerEndpoints:
    def get_sticker(self, sticker_id: int):
        r = Route("GET", "/stickers/{sticker_id}", sticker_id=sticker_id)
        return self.request(r)

    def list_nitro_sticker_packs(self):
        r = Route("GET", "/sticker-packs")
        return self.request(r)

    def list_guild_stickers(self, guild_id: int):
        r = Route("GET", "/guilds/{guild_id}/stickers", guild_id=guild_id)
        return self.request(r)

    def get_guild_sticker(self, guild_id: int, sticker_id: int):
        r = Route("GET", "/guilds/{guild_id}/stickers/{sticker_id}", guild_id=guild_id, sticker_id=sticker_id)
        return self.request(r)

    def create_sticker(self, guild_id: int, *, name: str, description: str, tags: str, file, reason: str = None):
        r = Route("POST", "/guilds/{guild_id}/stickers", guild_id=guild_id)
        payload = {
            "name": name,
            "description": description,
            "tags": tags,
        }
        form = self._prepare_form(payload, [file])
        return self.request(r, form=form, reason=reason)

    def edit_sticker(self, guild_id: int, sticker_id: int, *, name: str = MISSING, description: str = MISSING, tags: str = MISSING, reason: str = None):
        r = Route("PATCH", "/guilds/{guild_id}/stickers", guild_id=guild_id, sticker_id=sticker_id)
        payload = {
            "name": name,
            "description": description,
            "tags": tags,
        }

        if name is not MISSING:
            payload["name"] = name

        if description is not MISSING:
            payload["description"] = description

        if tags is not MISSING:
            payload["tags"] = tags

        return self.request(r, payload=payload, reason=reason)

    def delete_sticker(self, guild_id: int, sticker_id: int):
        r = Route("DELETE", "/guilds/{guild_id}/stickers/{sticker_id}", guild_id=guild_id, sticker_id=sticker_id)
        return self.request(r)
