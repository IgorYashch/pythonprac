import asyncio
import shlex
from collections import namedtuple
from io import StringIO

from cowsay import cowsay, list_cows, read_dot_cow

X_SHAPE, Y_SHAPE = 10, 10
PORT = 1337
HOST = "127.0.0.1"

# ----------------------------------------------
# --------------------SERVER--------------------
# ----------------------------------------------

custom_monster = read_dot_cow(
    StringIO(
        r"""
$the_cow = <<EOC;
        \\
         \\
    ,_    \\               _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\\\'--'//__
         (((""`  `"")))
EOC
"""
    )
)

Coords = namedtuple("Coords", ["x", "y"])
Coords.__repr__ = lambda self: f"({self.x}, {self.y})"


# Класс самой игры (Запускается на сервере, вход)
# Вход методов - только строки!!!
class MultiUserDungeon:
    shape = (0, 0)
    monsters_coords = {}
    user_coords = Coords(0, 0)

    def __init__(self, m, n):
        self.shape = (m, n)
        self.monsters = {}
        self.user_coords = Coords(0, 0)
        self.answer_message = ""

    def print(self, msg):
        self.answer_message += msg + "\n"

    def move(self, command):
        self.answer_message = ""

        cmds = {
            "up": Coords(1, 0),
            "down": Coords(-1, 0),
            "right": Coords(0, 1),
            "left": Coords(0, -1),
        }

        x = (self.user_coords.x + cmds[command].x) % X_SHAPE
        y = (self.user_coords.y + cmds[command].y) % Y_SHAPE
        self.user_coords = Coords(x, y)

        self.print(f"Moved to {self.user_coords}")

        if self.user_coords in self.monsters_coords:
            self.encounter(self.user_coords)

        return self.answer_message

    def encounter(self, monster_coords):
        monster, phrase, hp = self.monsters_coords[monster_coords]
        if monster == "jgsbat":
            self.print(cowsay(phrase, cowfile=custom_monster))
        else:
            self.print(cowsay(phrase, cow=monster))

    def add_monster(self, name, x, y, phrase, hp):
        self.answer_message = ""
        x, y, hp = int(x), int(y), int(hp)
        coords = Coords(x, y)

        if name not in [*list_cows(), "jgsbat"]:
            self.print("Cannot add unknown monster")
            return

        self.print(f'Added monster {name} to {coords} saying "{phrase}"')

        if coords in self.monsters_coords:
            self.print("Replace the old monster")

        self.monsters_coords[coords] = name, phrase, hp

        return self.answer_message

    def attack(self, weapon):
        self.answer_message = ""

        weapons_damage = {"sword": 10, "spear": 15, "axe": 20}

        if weapon not in weapons_damage:
            self.print("Unknown weapon")
            return self.answer_message
        damage = weapons_damage[weapon]

        if self.user_coords not in self.monsters_coords:
            self.print("No monster here")
        else:
            monster, phrase, hp = self.monsters_coords[self.user_coords]
            attack_hp = min(hp, damage)
            self.print(f"Attacked {monster}, damage {attack_hp} hp")
            new_hp = hp - attack_hp
            if new_hp:
                self.monsters_coords[self.user_coords] = monster, phrase, new_hp
                self.print(f"{monster} now has {new_hp}")
            else:
                del self.monsters_coords[self.user_coords]
                self.print(f"{monster} died")

        return self.answer_message

    def attack_by_name(self, monster_name):
        self.answer_message = ""
        if self.user_coords not in self.monsters_coords:
            self.print(f"No {monster_name} here")
        else:
            monster, phrase, hp = self.monsters_coords[self.user_coords]
            if monster == monster_name:
                self.attack("sword")
            else:
                self.print(f"No {monster_name} here")
        return self.answer_message


# Объект игры
game = None


# Основной обработчик сообщений от клиента
# Каждый раз образается к объекту game
async def handler(reader, writer):
    while not reader.at_eof():
        data = await reader.readline()

        method, *args = shlex.split(data.decode())
        print(method)
        answer = getattr(game, method)(*args) + "\n"
        print(answer)
        writer.write(answer.encode())
    writer.close()
    await writer.wait_closed()


async def main_server():
    server = await asyncio.start_server(handler, HOST, PORT)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    game = MultiUserDungeon(X_SHAPE, Y_SHAPE)
    asyncio.run(main_server())