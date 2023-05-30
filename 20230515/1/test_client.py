import unittest
from unittest.mock import MagicMock
from moodclient.moodclient.ClientCmd import MUD_mainloop

message = None


def foo(msg):
    global message
    message = msg.decode().rstrip()


class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sct = MagicMock()
        sct.sendall = foo
        cls.client_cmd = MUD_mainloop(sct, test=True)

    def test_0(self):
        self.client_cmd.do_attack("")
        self.assertEqual(message, "attack sword")

    def test_1(self):
        self.client_cmd.do_up('')
        self.assertEqual(message, "move up")

    def test_3(self):
        self.client_cmd.do_left('')
        self.assertEqual(message, "move left")

    def test_4(self):
        self.client_cmd.do_addmon('tortule coords 1 1 hp 1000 hello "I am tortule"')
        self.assertEqual(message, 'add_monster tortule 1 1 "I am tortule" 1000')

    def test_5(self):
        self.client_cmd.do_addmon('default hello "Moo" hp 10 coords 2 5')
        self.assertEqual(message, 'add_monster default 2 5 "Moo" 10')