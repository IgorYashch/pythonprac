"""
Модуль для командной строки клиента.
Этот модуль определяет командную строку MUD и все её команды.
"""

import cmd
import shlex
import readline
import threading
from cowsay import list_cows

# ----------------------------------------------
# --------------------CLIENT--------------------
# ----------------------------------------------


# Класс обработчика команд для клиента
# Обращается к клиенту и зависает, пока не получит ответ
class MUD_mainloop(cmd.Cmd):
    """
    Командная строка Multiuser Dungeon (MUD).
    Этот класс реализует командную строку для клиента MUD.
    """

    prompt = "(MUD) "

    def __init__(self, sct, test=False):
        """
        Инициализация командной строки.

        :param sct: Сокет для соединения с сервером.
        :type sct: socket.socket
        """
        super().__init__()
        self.sct = sct

        self.exit_event = threading.Event()
        self.test = test
        if not self.test:
            self.print_thread = threading.Thread(target=self.print_from_server)
            self.print_thread.start()

    def print_from_server(self):
        """
        Демон функция в отдельном потоке для вывода ответов сервера.

        :return: None
        """
        while True:
            msg = self.sct.recv(1024).decode().rstrip()
            print(
                f"\n{msg}\n{self.prompt}{readline.get_line_buffer()}",
                end="",
                flush=True,
            )

            if self.exit_event.is_set():
                break

    def do_up(self, args):
        """
        Двигаться вверх.

        :param args: Не используется.
        :return: None
        """
        self.sct.sendall(b"move up\n")

    def do_down(self, args):
        """
        Двигаться вниз.

        :param args: Не используется.
        :return: None
        """
        self.sct.sendall(b"move down\n")

    def do_left(self, args):
        """
        Двигаться влево.

        :param args: Не используется.
        :return: None
        """
        self.sct.sendall(b"move left\n")

    def do_right(self, args):
        """
        Двигаться вправо.

        :param args: Не используется.
        :return: None
        """
        self.sct.sendall(b"move right\n")

    def do_addmon(self, args):
        """
        Добавить монстра в игру.

        Формат:
            addmon <имя-монстра> coords <x> <y> hello <приветствие> hp <здоровье>
            (coords, hello и hp - можно поменять местами)

        :param args: строка аргументов.
        :return: None
        """
        try:
            shlex_line = shlex.split(args)
            if len(shlex_line) == 9:
                raise SyntaxError

            monster_name = shlex_line[0]

            coords_index = shlex_line.index("coords")
            coords = tuple(map(int, shlex_line[coords_index + 1 : coords_index + 3]))

            hello_index = shlex_line.index("hello")
            hello_message = shlex_line[hello_index + 1]

            hp_index = shlex_line.index("hp")
            hp = int(shlex_line[hp_index + 1])
        except Exception:
            print("Wrong format of command! Try again!")
        else:
            message = f'add_monster {monster_name} {coords[0]} {coords[1]} "{hello_message}" {hp}\n'
            self.sct.sendall(message.encode())

    def do_attack(self, args):
        """
        Атаковать монстра.
        Форматы: attack (<имя монстра>) (with <имя оружия>)
            
        :param args: строка аргументов.
        :return: None
        """

        args = shlex.split(args)
        if not args:
            message = "attack sword\n"
            self.sct.sendall(message.encode())

        elif len(args) == 2 and args[0] == "with":
            message = f"attack {args[1]}\n"
            self.sct.sendall(message.encode())

        elif len(args) == 1 and args[0] != "with":
            message = f"attack_by_name {args[0]} sword\n"
            self.sct.sendall(message.encode())

        elif len(args) == 3 and args[1] == "with":
            message = f"attack_by_name {args[0]} {args[2]}\n"
            self.sct.sendall(message.encode())
        else:
            print("Wrong format of command! Try again!")

    def do_sayall(self, args):
        """
        Отправить сообщение всем пользователям (включая вас самого).

        :param args: строка сообщения.
        :return: None
        """

        args = shlex.split(args)
        if len(args) != 1:
            print("Wrong format of command! Try again!")
        else:
            message = f'sayall "{args[0]}"\n'
            self.sct.sendall(message.encode())

    def do_quit(self, args):
        """
        Выйти из игры.

        :param args: Не используется.
        :return: True, чтобы остановить основной цикл.
        """
        self.sct.sendall("quit\n".encode())
        if not self.test:
            self.exit_event.set()
        return True

    do_EOF = do_quit

    def emptyline(self):
        """
        Действие при вводе пустой строки. По умолчанию ничего не делает.

        :return: None
        """
        pass

    def complete_attack(self, prefix, line, start, end):
        """
        Автозаполнение для команды атаки.

        :param prefix: введенный префикс строки.
        :param line: полная введенная строка.
        :param start: начальный индекс префикса в строке.
        :param end: конечный индекс префикса в строке.
        :return: список возможных вариантов для автозаполнения.
        """
        if "with" in line:
            return [x for x in ("sword", "spear", "axe") if x.startswith(prefix)]
        elif line.split()[-1] == "attack":
            return [x for x in [*list_cows(), "jgsbat"]]
        elif line.split()[1] == prefix:
            return [x for x in [*list_cows(), "jgsbat"] if x.startswith(prefix)]

    def complete_addmon(self, prefix, line, start, end):
        """
        Автозаполнение для команды добавления монстра.

        :param prefix: введенный префикс строки.
        :param line: полная введенная строка.
        :param start: начальный индекс префикса в строке.
        :param end: конечный индекс префикса в строке.
        :return: список возможных вариантов для автозаполнения.
        """
        if line.split()[-1] == "addmon":
            return [x for x in [*list_cows(), "jgsbat"]]
        elif line.split()[1] == prefix:
            return [x for x in [*list_cows(), "jgsbat"] if x.startswith(prefix)]
