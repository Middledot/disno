# disno
A modular API wrapper designed to handle the many aspects of the [Discord API](https://discord.dev).

What is meant by modular is that you can resuse components for other parts of the library or your custom implementations.

> The library is currently in early development.

## Is this a fork of discord.py?
This library does inspire greatly from [discord.py](https://github.com/Rapptz/discord.py)
but is essentially different and aims to implement features that discord.py didn't as well
as features it hasn't.

## Very Basic Example

```py
from disno import GatewayClient

client = GatewayClient()

@client.listener('ready')
async def on_ready(data):
    print(f"Logged in as {data['user']['username']} ({data['user']['id']})")

@client.listener()
async def message_create(data):
    if data["content"].startswith('>ping'):
        await client.http.send_message(data["channel_id"], content="works nice")

client.run("token")
```
