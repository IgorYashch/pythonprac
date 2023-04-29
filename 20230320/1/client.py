import cmd
import shlex
import socket
import readline
import threading
import sys
from cowsay import list_cows


X_SHAPE, Y_SHAPE = 10, 10
PORT = 1337
HOST = "127.0.0.1"


# ----------------------------------------------
# --------------------CLIENT--------------------
# ----------------------------------------------


# Класс обработчика команд для клиента
# Обращается к клиенту и зависает, пока не получит ответ
class MUD_mainloop(cmd.Cmd):
    intro = """<<< Welcome to Python-MUD 0.2 >>>"""
    prompt = "(MUD) "

    def __init__(self, sct):
        super().__init__()
        self.sct = sct

        self.print_thread = threading.Thread(target=self.print_from_server)
        self.print_thread.start()

    def print_from_server(self):
        "Daemon function in another thread for printing answers"
        while True:
            msg = self.sct.recv(1024).decode().rstrip()
            print(
                f"\n{msg}\n{self.prompt}{readline.get_line_buffer()}",
                end="",
                flush=True,
            )

    def do_up(self, args):
        """Move up"""
        self.sct.sendall(b"move up\n")

    def do_down(self, args):
        """Move down"""
        self.sct.sendall(b"move down\n")

    def do_left(self, args):
        """Move left"""
        self.sct.sendall(b"move left\n")

    def do_right(self, args):
        """Move right"""
        self.sct.sendall(b"move right\n")

    def do_addmon(self, line):
        """
        Add monster to the game
        Format:
            addmon <monster-name> coords <x> <y> hello <hello message> hp <heatpoints>
            (coords, hello and hp - can be swaped)
        """
        try:
            shlex_line = shlex.split(line)
            if len(shlex_line) == 9:
                raise SyntaxError

            monster_name = shlex_line[0]

            coords_index = shlex_line.index("coords")
            coords = tuple(map(int, shlex_line[coords_index + 1 : coords_index + 3]))

            hello_index = shlex_line.index("hello")
            hello_message = shlex_line[hello_index + 1]

            hp_index = shlex_line.index("hp")
            hp = int(shlex_line[hp_index + 1])
        except:
            print("Wrong format of command! Try again!")
        else:
            message = f'add_monster {monster_name} {coords[0]} {coords[1]} "{hello_message}" {hp}\n'
            self.sct.sendall(message.encode())

    def do_attack(self, args):
        """
        Attack monster 
        Formats: 
            - attack [<monster's name>] [with <weapon's name>]
        """
        args = shlex.split(args)
        if not args:
            message = f"attack sword\n"
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
    
    def do_quit():
        """Quit the game"""
        return True
        
    def complete_attack(self, prefix, line, start, end):
        # print ("---", prefix)
        # print("---", line.split())
        if "with" in line:
            return [x for x in ("sword", "spear", "axe") if x.startswith(prefix)]
        elif (line.split()[-1] == 'attack'):
            return [x for x in [*list_cows(), "jgsbat"]]
        elif (line.split()[-1] == prefix):
            return [x for x in [*list_cows(), "jgsbat"] if x.startswith(prefix)]


def main():
    if len(sys.argv) != 2:
        print("Enter your user name")
    else:
        username = sys.argv[1]
        print(username)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            s.sendall((username + "\n").encode())
            message = s.recv(1024).decode()

            print(message)

            if message == "Connection created!":
                cmd = MUD_mainloop(s)
                cmd.cmdloop()
            else:
                return


if __name__ == "__main__":
    main()
