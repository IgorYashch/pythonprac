
import shlex
import cmd
from cowsay import cowsay, list_cows, read_dot_cow
from collections import namedtuple
from io import StringIO

custom_monster = read_dot_cow(StringIO(r"""
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
"""))

Coords = namedtuple('Coords', ['x', 'y'])
Coords.__repr__ = lambda self: f'({self.x}, {self.y})'

X_SHAPE, Y_SHAPE = 10, 10
DEFAULT_ATTACH_HP = 10

class MultiUserDungeon:
    shape = (0, 0)
    monsters_coords = {}
    user_coords = Coords(0, 0)

    def __init__(self, m, n):
        self.shape = (m, n)
        self.monsters = {}
        self.user_coords = Coords(0, 0)

    def move(self, command):
        cmds = {
            "up": Coords(1, 0),
            "down": Coords(-1, 0),
            "right": Coords(0, 1),
            "left": Coords(0, -1),
        }

        x = (self.user_coords.x + cmds[command].x) % X_SHAPE
        y = (self.user_coords.y + cmds[command].y) % Y_SHAPE
        self.user_coords = Coords(x, y)
        print(f"Moved to {self.user_coords}")

        if self.user_coords in self.monsters_coords:
            self.encounter(self.user_coords)

    def add_monster(self, name, x, y, phrase, hp):
        coords = Coords(x, y)

        if name not in [*list_cows(), 'jgsbat']:
            print('Cannot add unknown monster')
            return

        print(f"Added monster {name} to {coords} saying \"{phrase}\"")

        if coords in self.monsters_coords:
            print("Replace the old monster")

        self.monsters_coords[coords] = name, phrase, hp

    def encounter(self, monster_coords):
        monster, phrase, hp = self.monsters_coords[monster_coords]
        if monster == 'jgsbat':
            print(cowsay(phrase, cowfile=custom_monster))
        else:
            print(cowsay(phrase, cow=monster))
    
    def attack(self):
        if self.user_coords not in self.monsters_coords:
            print("No monster here")
        else:
            monster, phrase, hp = self.monsters_coords[self.user_coords]
            attack_hp = min(hp, DEFAULT_ATTACH_HP)
            print(f'Attacked {monster}, damage {attack_hp} hp')
            new_hp = hp - attack_hp
            if new_hp:
                self.monsters_coords[self.user_coords] = monster, phrase, new_hp
                print(f'{monster} now has {new_hp}')
            else:
                del self.monsters_coords[self.user_coords]
                print(f'{monster} died')

class MUD_mainloop(cmd.Cmd):
    intro = """<<< Welcome to Python-MUD 0.1 >>>"""
    prompt = "(MUD) "

    def __init__(self, n, m):
        super().__init__()
        self.game = MultiUserDungeon(n, m)

    def do_up(self, args):
        self.game.move('up')

    def do_down(self, args):
        self.game.move('down')

    def do_left(self, args):
        self.game.move('left')

    def do_right(self, args):
        self.game.move('right')

    def do_addmon(self, line):
        try:
            shlex_line = shlex.split(line)
            if len(shlex_line) == 9:
                raise SyntaxError

            monster_name = shlex_line[0]

            coords_index = shlex_line.index('coords')
            coords = tuple(
                map(int, shlex_line[coords_index + 1:coords_index + 3]))

            hello_index = shlex_line.index('hello')
            hello_message = shlex_line[hello_index + 1]

            hp_index = shlex_line.index('hp')
            hp = int(shlex_line[hp_index + 1])
        except:
            print("Wrong format of command! Try again!")
        else:
            self.game.add_monster(monster_name, *coords, hello_message, hp)

    def do_attack(self, args):
        if not args:
            self.game.attack()

if __name__ == "__main__":
    loop = MUD_mainloop(10, 10)
    loop.cmdloop()
