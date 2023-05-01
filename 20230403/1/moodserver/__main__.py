"""Entrypoint for the server"""

import asyncio

from .Server import MultiUserDungeon, handler, move_random_monster
from .Server import X_SHAPE, Y_SHAPE

PORT = 1337
HOST = "127.0.0.1"

MONSTER_MOVE_INTERVAL = 30


async def main_server():
    """Main function for server."""
    # Класс самой игры
    game = MultiUserDungeon(X_SHAPE, Y_SHAPE)
    # Словарь с очередями на отправку сообщений пользователям
    clients = {}
    
    server = await asyncio.start_server(lambda r, w: handler(r, w, game, clients), HOST, PORT)
        
    await asyncio.gather(server.serve_forever(),
                         move_random_monster(game, clients, MONSTER_MOVE_INTERVAL)
                        )


asyncio.run(main_server())
