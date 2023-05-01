"""Entrypoint for the server"""

import asyncio

from .Server import MultiUserDungeon, handler
from .Server import X_SHAPE, Y_SHAPE

PORT = 1337
HOST = "127.0.0.1"


async def main_server():
    """Main function for server."""
    game = MultiUserDungeon(X_SHAPE, Y_SHAPE)
    clients = {}
    server = await asyncio.start_server(lambda r, w: handler(r, w, game, clients), HOST, PORT)
    async with server:
        await server.serve_forever()


asyncio.run(main_server())
