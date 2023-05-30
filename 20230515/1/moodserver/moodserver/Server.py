"""Модуль с обработчиком сервера asyncio и классом игры MultiUserDungeon."""

import asyncio
import shlex
import random
import time
from io import StringIO

from cowsay import cowsay, list_cows, read_dot_cow
from .UserCoords import Coordinates

X_SHAPE, Y_SHAPE = 10, 10


SEND_ONE_USER = 0
SEND_ANOTHER_USERS = 1
SEND_ALL_USERS = 2

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
    """
    Класс, реализующий многопользовательскую игру в стиле подземелья.

    Ответственен за управление всей логикой игры, включая управление пользователями и монстрами.
    """
    shape = (0, 0)

    def __init__(self, m, n):
        """
        Инициализирует новую игру с заданной формой.

        :param m: Количество строк в игре.
        :type m: int
        :param n: Количество столбцов в игре.
        :type n: int
        """
        self.shape = (m, n)

        # Formant: {<coords>: (<monster_name>, <phrase>, <hp>)}
        self.monsters = {}

        # Formant: {<name> :  <coords>}
        self.users_coords = {}

        # Format: [(<message>: string, <for all users?>: int, <to_username>: string)]
        self.answer_messages = []
        
        self.cmds = {
            "up": (1, 0),
            "down": (-1, 0),
            "right": (0, 1),
            "left": (0, -1),
        }

    def add_new_user(self, username):
        """
        Добавляет нового пользователя в игру.

        :param username: Имя пользователя.
        :type username: str
        """
        self.answer_messages = []
        self.users_coords[username] = Coordinates(0, 0, self.shape)
        self.print(f"{username} enter to the game!", SEND_ANOTHER_USERS, username)
        return self.answer_messages

    def quit(self, username):
        """
        Удаляет пользователя из игры.

        :param username: Имя пользователя.
        :type username: str
        """
        self.answer_messages = []
        del self.users_coords[username]
        self.print(f"Googdye, {username}!", SEND_ONE_USER, username)
        self.print(f"User {username} quit the game!", SEND_ANOTHER_USERS, username)
        return self.answer_messages

    def check_user(self, username):
        """
        Проверяет, есть ли пользователь с таким именем уже в игре.

        :param username: Имя пользователя.
        :type username: str
        :return: True если пользователь в игре, иначе False.
        :rtype: bool
        """
        return username in self.users_coords

    def print(self, msg, mode, to_username=None):
        """
        Добавляет сообщение в список результата ответов.
        (Внутренняя функция)

        :param msg: Сообщение.
        :type msg: str
        :param mode: Режим отправки.
        :type mode: int
        :param to_username: Имя пользователя, которому отправляется сообщение.
        :type to_username: str, optional
        """
        self.answer_messages.append((msg + "\n", mode, to_username))

    def move(self, username, command):
        """
        Перемещает пользователя.

        :param username: Имя пользователя.
        :type username: str
        :param command: Команда для перемещения.
        :type command: str
        """
        self.answer_messages = []

        self.users_coords[username] += self.cmds[command]

        self.print(f"Moved to {self.users_coords[username]}", SEND_ONE_USER, username)

        if self.users_coords[username] in self.monsters:
            self.encounter(username, self.users_coords[username])

        return self.answer_messages

    def encounter(self, username, monster_coords):
        """
        Встреча с монстром.

        :param username: Имя пользователя.
        :type username: str
        :param monster_coords: Координаты монстра.
        :type monster_coords: tuple
        """
        monster, phrase, hp = self.monsters[monster_coords]
        if monster == "jgsbat":
            self.print(cowsay(phrase, cowfile=custom_monster), SEND_ONE_USER, username)
        else:
            self.print(cowsay(phrase, cow=monster), SEND_ONE_USER, username)

    def add_monster(self, username, name, x, y, phrase, hp):
        """
        Добавляет нового монстра в игру.

        :param username: Имя пользователя.
        :type username: str
        :param name: Имя монстра.
        :type name: str
        :param x: Координата X монстра.
        :type x: int
        :param y: Координата Y монстра.
        :type y: int
        :param phrase: Фраза монстра.
        :type phrase: str
        :param hp: Здоровье монстра.
        :type hp: int
        """
        self.answer_messages = []
        x, y, hp = int(x), int(y), int(hp)
        coords = Coordinates(x, y, self.shape)

        if name not in [*list_cows(), "jgsbat"]:
            self.print("Cannot add unknown monster", SEND_ONE_USER, username)
            return

        self.print(f'{username} added monster {name} to {coords} saying "{phrase}"', SEND_ANOTHER_USERS, username)
        self.print(f'Added monster {name} to {coords} saying "{phrase}"', SEND_ONE_USER, username)

        if coords in self.monsters:
            self.print("The old monster was replaced", SEND_ALL_USERS)

        self.monsters[coords] = name, phrase, hp

        return self.answer_messages

    def attack(self, username, weapon):
        """
        Атакует монстра в текущей позиции.

        :param username: Имя пользователя.
        :type username: str
        :param weapon: Оружие для атаки.
        :type weapon: str
        """
        self.answer_messages = []

        weapons_damage = {"sword": 10, "spear": 15, "axe": 20}

        if weapon not in weapons_damage:
            self.print("Unknown weapon", SEND_ONE_USER, username)
            return self.answer_messages

        damage = weapons_damage[weapon]

        if self.users_coords[username] not in self.monsters:
            self.print("No monster here", SEND_ONE_USER, username)
        else:
            monster, phrase, hp = self.monsters[self.users_coords[username]]
            attack_hp = min(hp, damage)

            new_hp = hp - attack_hp

            self.print(f"Attacked {monster}, damage {attack_hp} hp", SEND_ONE_USER, username)
            self.print(f"User {username} attacked {monster}, damage {attack_hp} hp", SEND_ANOTHER_USERS, username)
            if new_hp:
                self.monsters[self.users_coords[username]] = monster, phrase, new_hp
                self.print(f"Monster {monster} now has {new_hp}", SEND_ALL_USERS)
            else:
                del self.monsters[self.users_coords[username]]
                self.print(f"Monster {monster} died", SEND_ALL_USERS)

        return self.answer_messages

    def attack_by_name(self, username, monster_name, weapon):
        """
        Атакует монстра с заданным именем в текущей позиции.

        :param username: Имя пользователя.
        :type username: str
        :param monster_name: Имя монстра для атаки.
        :type monster_name: str
        :param weapon: Оружие для атаки.
        :type weapon: str
        :return: Ответные сообщения.
        :rtype: list
        """
        self.answer_messages = []
        if self.users_coords[username] not in self.monsters:
            self.print(f"No {monster_name} here", SEND_ONE_USER, username)
        else:
            monster, phrase, hp = self.monsters[self.users_coords[username]]
            if monster == monster_name:
                self.attack(username, weapon)
            else:
                self.print(f"No {monster_name} here", SEND_ONE_USER, username)
        return self.answer_messages

    def sayall(self, username, message):
        """
        Отправляет сообщение всем другим пользователям.

        :param username: Имя пользователя.
        :type username: str
        :param message: Сообщение для отправки.
        :type message: str
        :return: Ответные сообщения.
        :rtype: list
        """
        
        self.answer_messages = []
        self.print(f"{username}: " + message, SEND_ALL_USERS)
        return self.answer_messages

    def move_monster(self):
        """
        Перемещает случайного монстра в случайном направлении на одну клетку.

        :return: Ответные сообщения.
        :rtype: list
        """
        self.answer_messages = []

        if not self.monsters:
            return self.answer_messages
        
        random_monster_coords = random.choice(list(self.monsters))
        random_move = random.choice(list(self.cmds))

        monster_info = self.monsters[random_monster_coords]
        monster_name = monster_info[0]

        new_coords = random_monster_coords + self.cmds[random_move]
        self.monsters[new_coords] = monster_info
        del self.monsters[random_monster_coords]

        self.print(f'{monster_name} moved one cell {random_move}', SEND_ALL_USERS)

        for user, coords in self.users_coords.items():
            if new_coords == coords:
                self.encounter(user, new_coords)

        return self.answer_messages


async def handler(reader, writer, game, clients):
    """
    Асинхронная функция-обработчик для пользовательских сессий.

    Отвечает за обработку пользовательских команд и отправку сообщений пользователям.

    :param reader: Средство чтения asyncio, используемое для чтения данных от пользователя.
    :type reader: StreamReader
    :param writer: Средство записи asyncio, используемое для отправки данных пользователю.
    :type writer: StreamWriter
    :param game: Экземпляр игры MultiUserDungeon, который содержит всю игровую логику.
    :type game: MultiUserDungeon
    :param clients: Словарь клиентов с их очередями сообщений.
    :type clients: dict
    """
    username = await reader.readline()
    username = username.decode().rstrip()

    if not game.check_user(username):

        messages = game.add_new_user(username)
        for user_queue in clients.values():
            await user_queue.put(messages[0][0])

        writer.write("Connection created!".encode())

        clients[username] = asyncio.Queue()

        # Инициируем процессы чтения команды клиента и чтения из очереди для отправки
        read_command = asyncio.create_task(reader.readline())
        get_message = asyncio.create_task(clients[username].get())

        while not reader.at_eof():
            done, _ = await asyncio.wait([read_command, get_message], return_when=asyncio.FIRST_COMPLETED)

            for job in done:
                if job is read_command:
                    # Запускаем новое чтение на обработку
                    read_command = asyncio.create_task(reader.readline())

                    # Обрабатываем запрос и отправляем в нужные очереди для отправки клиентам
                    data = job.result()
                    method, *args = shlex.split(data.decode())
                    print(f'{username}: {method}')
                    answers = getattr(game, method)(username, *args)
                    
                    # Отправить всем, кому надо
                    for message, mode, to_username in answers:
                        if mode == SEND_ONE_USER:
                            await clients[to_username].put(message)
                        else:
                            for user, user_queue in clients.items():
                                if mode == SEND_ANOTHER_USERS and user == to_username:
                                    continue
                                await user_queue.put(message)

                    if method == 'quit':
                        writer.write(answers[0][0].encode())
                        break

                elif job is get_message:
                    # Запускаем новое стение сообщений на отправку
                    get_message = asyncio.create_task(clients[username].get())

                    # Отправляем полученное сообщение
                    writer.write(job.result().encode())
                    await writer.drain()

        del clients[username]

    else:
        writer.write("User already exist!".encode())

    writer.close()
    await writer.wait_closed()


async def move_random_monster(game, clients, time_interval):
    """
    Демон функция для перемещения одного случайного монстра с заданным временным интервалом.

    :param game: Экземпляр игры MultiUserDungeon, который содержит всю игровую логику.
    :type game: MultiUserDungeon
    :param clients: Словарь клиентов с их очередями сообщений.
    :type clients: dict
    :param time_interval: Временной интервал в секундах между перемещениями монстров.
    :type time_interval: int
    """
    while True:
        await asyncio.sleep(time_interval)
        answers = game.move_monster()
        for message, mode, to_username in answers:
            if mode == SEND_ONE_USER:
                await clients[to_username].put(message)
            else:
                for user, user_queue in clients.items():
                    if mode == SEND_ANOTHER_USERS and user == to_username:
                        continue
                    await user_queue.put(message)