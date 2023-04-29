import asyncio
import shlex
from io import StringIO

from cowsay import cowsay, list_cows, read_dot_cow
from user_coords import Coordinates

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


# Класс самой игры (Запускается на сервере, вход)
# Вход методов - только строки!!!
class MultiUserDungeon:
    shape = (0, 0)

    def __init__(self, m, n):
        """Init game"""
        self.shape = (m, n)
        
        # Formant: {<coords>: (<monster_name>, <phrase>, <hp>)}
        self.monsters = {}
        
        # Formant: {<name> :  <coords>}
        self.users_coords = {}
        
        # Format: [(<for all users?>: bool, <message>: string)]
        self.answer_messages = []
        
    def add_new_user(self, username):
        """Add new user to the game"""
        self.users_coords[username] = Coordinates(0, 0, self.shape)
        
    def check_user(self, username):
        """Check if user already in the game"""
        return username in self.users_coords

    def print(self, msg, mode):
        """Add message to the list of result answers.
        mode: True - send to all users
        (Private function)
        """
        self.answer_messages.append((msg + "\n", mode))

    def move(self, username, command):
        """Move user"""
        self.answer_messages = []

        cmds = {
            "up": (1, 0),
            "down": (-1, 0),
            "right": (0, 1),
            "left": (0, -1),
        }

        self.users_coords[username] += cmds[command]

        self.print(f"Moved to {self.users_coords[username]}", False)

        if self.users_coords[username] in self.monsters:
            self.encounter(self.users_coords[username])

        return self.answer_messages

    def encounter(self, monster_coords):
        """Meeting with monster"""
        monster, phrase, hp = self.monsters[monster_coords]
        if monster == "jgsbat":
            self.print(cowsay(phrase, cowfile=custom_monster), False)
        else:
            self.print(cowsay(phrase, cow=monster), False)

    def add_monster(self, username, name, x, y, phrase, hp):
        """Add new monster to the game"""
        self.answer_messages = []
        x, y, hp = int(x), int(y), int(hp)
        coords = Coordinates(x, y, self.shape)

        if name not in [*list_cows(), "jgsbat"]:
            self.print("Cannot add unknown monster", False)
            return

        self.print(f'Added monster {name} to {coords} saying "{phrase}"', True)

        if coords in self.monsters:
            self.print("Replace the old monster", True)

        self.monsters[coords] = name, phrase, hp

        return self.answer_messages

    def attack(self, username, weapon):
        """Attack monster in current position"""
        self.answer_messages = []

        weapons_damage = {"sword": 10, "spear": 15, "axe": 20}

        if weapon not in weapons_damage:
            self.print("Unknown weapon", False)
            return self.answer_messages
        
        damage = weapons_damage[weapon]

        if self.users_coords[username] not in self.monsters:
            self.print("No monster here", False)
        else:
            monster, phrase, hp = self.monsters[self.users_coords[username]]
            attack_hp = min(hp, damage)
            self.print(f"Attacked {monster}, damage {attack_hp} hp", True)
            new_hp = hp - attack_hp
            if new_hp:
                self.monsters[self.users_coords[username]] = monster, phrase, new_hp
                self.print(f"{monster} now has {new_hp}", True)
            else:
                del self.monsters[self.users_coords[username]]
                self.print(f"{monster} died", True)

        return self.answer_messages

    def attack_by_name(self, username, monster_name):
        self.answer_messages = []
        if self.users_coords not in self.monsters:
            self.print(f"No {monster_name} here", False)
        else:
            monster, phrase, hp = self.monsters[self.users_coords[username]]
            if monster == monster_name:
                self.attack(username, "sword")
            else:
                self.print(f"No {monster_name} here", False)
        return self.answer_messages


# Объект игры
game = None


clients = {}

async def handler(reader, writer):
    username = await reader.readline()
    username = username.decode().rstrip()

    if not game.check_user(username):
        game.add_new_user(username)
        writer.write("Connection created!".encode())

        clients[username] = asyncio.Queue()

        # Инициируем процессы чтения команды клиента и чтения из очереди для отправки
        read_command = asyncio.create_task(reader.readline())
        get_message = asyncio.create_task(clients[username].get())

        while not reader.at_eof():
            done, pending = await asyncio.wait([read_command, get_message], return_when=asyncio.FIRST_COMPLETED)

            for job in done:
                if job is read_command:
                    # Запускаем новое чтение на обработку
                    read_command = asyncio.create_task(reader.readline())

                    # Обрабатываем запрос и отправляем в нужные очереди для отправки клиентам
                    data = job.result()
                    method, *args = shlex.split(data.decode())
                    answers = getattr(game, method)(username, *args)
                    for message, mode in answers:
                        if not mode:
                            await clients[username].put(message)
                        else:
                            for user_queue in clients.values():
                                await user_queue.put(message)

                elif job is get_message:
                    # Запускаем новое стение сообщений на отправку
                    get_message = asyncio.create_task(clients[username].get())

                    # Отправляем полученное сообщение
                    writer.write(job.result().encode())
                    await writer.drain()
            
    else:
        writer.write("User already exist!".encode())
        
    writer.close()
    await writer.wait_closed()


async def main_server():
    server = await asyncio.start_server(handler, HOST, PORT)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    game = MultiUserDungeon(X_SHAPE, Y_SHAPE)
    asyncio.run(main_server())
    
    
    