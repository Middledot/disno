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

from base64 import b64encode
from urllib.parse import quote as uriquote

try:
    import orjson

    to_json = lambda o: orjson.dumps(o).decode('utf-8')
    from_json = orjson.loads
except ModuleNotFoundError:
    import json

    to_json = lambda o: json.dumps(o, separators=(',', ':'), ensure_ascii=True)
    from_json = json.loads


class _MissingSentinel:
    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True

    def __repr__(self):
        return "<nothing here>"

MISSING = _MissingSentinel()


def get_mime_type_for_image(data: bytes):
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif data[0:3] == b'\xff\xd8\xff' or data[6:10] in (b'JFIF', b'Exif'):
        return 'image/jpeg'
    elif data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'image/gif'
    elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'image/webp'
    else:
        raise TypeError('Unsupported image type given')


def bytes_to_base64_data(data: bytes):
    mime = get_mime_type_for_image(data)
    b64 = b64encode(data).decode('ascii')
    return 'data:{mime};base64,{data}'.format(mime=mime, data=b64)
