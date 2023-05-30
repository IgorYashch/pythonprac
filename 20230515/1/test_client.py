import unittest
from unittest.mock import MagicMock
from moodclient.moodclient.ClientCmd import MUD_mainloop


class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = MagicMock()
        cls.client_cmd = MUD_mainloop()
        cls.player.__init__ = lambda args: None
        cls.player.send = lambda obj, command: setattr(cls.server, 'command', command)
        cls.game = cls.player()

    def test_0(self):
        self.game.do_attack('banana')
        self.assertEqual(self.server.command, 'attack banana sword 10')

    def test_1(self):
        self.game.do_attack('banana with spear')
        self.assertEqual(self.server.command, 'attack banana spear 15')

    def test_2(self):
        self.game.do_up('')
        self.assertEqual(self.server.command, 'move 0 -1')

    def test_3(self):
        self.game.do_left('')
        self.assertEqual(self.server.command, 'move -1 0')

    def test_4(self):
        self.server.command = ''
        self.game.do_addmon('shrek coords 1 1 hp 1000 hello hello')
        self.assertEqual(self.server.command, '')
