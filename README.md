# disno
A library for my experiments with the discord API

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
