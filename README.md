# PyCordHTTPServer

``PyCordHTTPServer`` allows for efficient an intuitive creation and management of an HTTP web server that runs alongside a py-cord bot.

# Key Features
- Easy to use , yet powerful API the makes spinning up a web server on the same event loop as discord.py bot painless
- Supports reloading on cog reload

# Getting Started
Here some examples how to use this API:

### Global Scope
````python
import discord
import server
from aiohttp import web

bot = discord.Bot(command_prefix="?", description="Example", intents=discord.Intents.all())

@bot.event
async def on_ready():
    bot.server = server.HTTPServer(
        bot=bot,
        host="0.0.0.0",
        port=8000,
    )
    await bot.server.start()

@server.add_route(path="/", method="GET")
async def home(request):
    return web.json_response(data={"foo": "bar"}, status=200)

bot.run("YOUR_TOKEN")
````

### Inside Bot Subclass
```python
import discord
import server
from aiohttp import web


class Bot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server = server.HTTPServer(
            bot=self,
            host="0.0.0.0",
            port=1337,
        )
        self.loop.create_task(self._start_webserver())
        

    async def _start_webserver(self):
        await self.wait_until_ready()
        await self.server.start()

    @server.add_route(path="/", method="GET")
    async def home(self, request):
        return web.json_response(data={"foo": bar}, status=200)

bot = Bot(command_prefix="!", description="example", intents=discord.Intents.all())
bot.run("YOUR_TOKEN")
```

### Inside Cog
```python

import server
import discord
from discord.ext import commands
from aiohttp import web

class ServerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.server = server.HTTPServer(
            bot=self.bot,
            host="0.0.0.0",
            port=8000
        )
        self.bot.loop.create_task(self._start_server())
        
    async def _start_server(self):
        await self.bot.wait_until_ready()
        await self.server.start()
    
    @server.add_route(path="/", method="GET", cog="ServerCog")
    async def home(self, request):
        return web.json_response(data={"foo": "bar"}, status=200)
```

### Using Checks with Globally Defined Methods
```python
import discord
import server
from aiohttp import web, ClientRequest

bot = discord.Bot(command_prefix="?", description="Example", intents=discord.Intents.all())

@bot.event
async def on_ready():
    bot.server = server.HTTPServer(
        bot=bot,
        host="0.0.0.0",
        port=1337,
    )
    await bot.server.start()

async def checker(request: ClientRequest):
    return request.headers.get("authorization") == "YourPassword"

async def fail_handler(request: ClientRequest):
    return web.json_response(data={"message": "You are not authorized"}, status=401)

@server.add_route(path="/", method="GET")
@server.check(predicate=checker, fail_handler=fail_handler)
async def home(request: ClientRequest):
    return web.json_response(data={"foo": "bar"}, status=200)

bot.run("YOUR_TOKEN")
```

### Using Checks with Cog Defined Methods
```python
import server
from aiohttp import web, ClientRequest
from discord.ext import commands

class ServerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.server = server.HTTPServer(
            bot=self.bot,
            host="0.0.0.0",
            port=1337,
        )
        self.bot.loop.create_task(self._start_server())

    async def _start_server(self):
        await self.bot.wait_until_ready()
        await self.server.start()

    async def checker(self, request: ClientRequest):
        return request.headers.get("authorization") == "YOur Password"

    async def fail_handler(self, request: ClientRequest):
        return web.json_response(data={"message": "You failed the Authorization"}, status=401)

    @server.add_route(path="/", method="GET", cog="ServerCog")
    @server.check(predicate="checker", fail_handler="fail_handler")
    async def home(self, request: ClientRequest):
        return web.json_response(data={"foo": "bar"}, status=200)
```
