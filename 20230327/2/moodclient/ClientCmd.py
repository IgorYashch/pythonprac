"""Module for comandline for client."""

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
    """Client command line."""
    prompt = "(MUD) "

    def __init__(self, sct):
        """Initialize of command line."""
        super().__init__()
        self.sct = sct

        self.print_thread = threading.Thread(target=self.print_from_server)
        self.exit_event = threading.Event()

        self.print_thread.start()

    def print_from_server(self):
        """Daemon function in another thread for printing server responses."""
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
        """Move up."""
        self.sct.sendall(b"move up\n")

    def do_down(self, args):
        """Move down."""
        self.sct.sendall(b"move down\n")

    def do_left(self, args):
        """Move left."""
        self.sct.sendall(b"move left\n")

    def do_right(self, args):
        """Move right."""
        self.sct.sendall(b"move right\n")

    def do_addmon(self, args):
        """
        Add monster to the game.

        Format:
            addmon <monster-name> coords <x> <y> hello <hello message> hp <heatpoints>
            (coords, hello and hp - can be swaped)
        """
        try:
            shlex_line = shlex.split(args)
            if len(shlex_line) == 9:
                raise SyntaxError

            monster_name = shlex_line[0]

            coords_index = shlex_line.index("coords")
            coords = tuple(map(int, shlex_line[coords_index + 1: coords_index + 3]))

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
        """Attack monster.
        Formats:
            attack [<monster's name>] [with <weapon's name>]
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
        """Send message to all users (including yourself)."""

        args = shlex.split(args)
        if len(args) != 1:
            print("Wrong format of command! Try again!")
        else:
            message = f"sayall \"{args[0]}\"\n"
            self.sct.sendall(message.encode())

    def do_quit(self, args):
        """Quit the game."""

        self.sct.sendall("quit\n".encode())
        self.exit_event.set()
        return True

    def complete_attack(self, prefix, line, start, end):
        """Complete attack command"""
        if "with" in line:
            return [x for x in ("sword", "spear", "axe") if x.startswith(prefix)]
        elif (line.split()[-1] == 'attack'):
            return [x for x in [*list_cows(), "jgsbat"]]
        elif (line.split()[1] == prefix):
            return [x for x in [*list_cows(), "jgsbat"] if x.startswith(prefix)]

    def complete_addmon(self, prefix, line, start, end):
        """Complete addmon command"""
        if (line.split()[-1] == 'addmon'):
            return [x for x in [*list_cows(), "jgsbat"]]
        elif (line.split()[1] == prefix):
            return [x for x in [*list_cows(), "jgsbat"] if x.startswith(prefix)]
