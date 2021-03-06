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

from .guilds import GuildEndpoints
from .users import UserEndpoints
from .oauth2 import OAuth2Endpoints
from .messages import MessageEndpoints
from .channels import ChannelEndpoints
from .messages import MessageEndpoints
from .reactions import ReactionEndpoints
from .commands import ApplicationCommandEndpoints
from .interactions import InteractionEndpoints
from .webhooks import WebhookEndpoints, AuthenticationlessWebhookEndpoints
from .scheduled_events import ScheduledEventEndpoints
from .templates import TemplateEndpoints
from .stage_instances import StageInstanceEndpoints
from .stickers import StickerEndpoints
from .voice import VoiceEndpoints

__all__ = (
    'GuildEndpoints',
    'ChannelEndpoints',
    'MessageEndpoints',
    'ReactionEndpoints',
    'UserEndpoints',
    'OAuth2Endpoints',
    'ApplicationCommandEndpoints',
    'InteractionEndpoints',
    'WebhookEndpoints',
    'AuthenticationlessWebhookEndpoints',
    'ScheduledEventEndpoints',
    'TemplateEndpoints',
    'StageInstanceEndpoints',
    'StickerEndpoints',
    'VoiceEndpoints',
)
