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

    def add_monster(self, name, x, y, phrase):
        coords = Coords(x, y)

        
        if name not in [*list_cows(), 'jgsbat']:
            print('Cannot add unknown monster')
            return

        print(f"Added monster {name} to {coords} saying \"{phrase}\"")

        if coords in self.monsters_coords:
            print("Replace the old monster")

        self.monsters_coords[coords] = name, phrase

    def encounter(self, monster_coords):
        monster, phrase = self.monsters_coords[monster_coords]
        if monster == 'jgsbat':
            print(cowsay(phrase, cowfile=custom_monster))
        else:
            print(cowsay(phrase, cow=monster))


def mainloop():
    
    game = MultiUserDungeon(10, 10)

    while (line:= input().split()):
        if not line:
            continue
        elif line[0] in {"up", "down", "left", "right"}:
            if len(line) > 1:
                raise SyntaxError("Invalid arguments")

            game.move(line[0])

        elif line[0] == "addmon":
            try:
                assert len(line) == 5
                line[2] = int(line[2])
                line[3] = int(line[3])
            except:
                raise SyntaxError("Invalid arguments")

            game.add_monster(*line[1:])

        else:
            raise ValueError("Invalid command")


if __name__ == "__main__":
    try:
        mainloop()
    except EOFError:
        exit()
    except Exception as e:
        print(e.args[0])
