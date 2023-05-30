import unittest
import socket
import multiprocessing
import time
import subprocess
import sys
import os
from moodclient.ClientCmd import MUD_mainloop
from moodclient.__main__ import HOST, PORT

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Запускаем сервер в отдельном процессе
        cls.server_proc = subprocess.Popen([sys.executable, '-m', 'moodserver'])

        # Ждем, чтобы сервер полностью запустился
        time.sleep(1)

        # print("hello")
        # Создаем клиента
        print(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(2)
        s.connect((HOST, PORT))
        print(3)
        s.sendall(("Igor\n").encode())
        message = s.recv(1024).decode()
        print(message)
        cls.client_cmd = MUD_mainloop(s, test=True)


    @classmethod
    def tearDownClass(cls):
        # Завершаем работу сервера
        os.kill(cls.server_proc.pid, signal.SIGTERM)

        # Закрываем соединение клиента
        cls.client_cmd.do_quit('')

    def test_setup_monster(self):
        # print(5)
        self.client_cmd.do_addmon('addmon default hello "Hello world" hp 25 coords 0 9')
        response = self.client_cmd.sct.recv(1024).decode()
        print(response)
        self.assertEqual(response.strip(), 'Added monster default to (9, 0) saying "Hello world"')
        # print(55)

    def test_approach_monster(self):
        # print(6)
        self.client_cmd.do_left('')
        response = self.client_cmd.sct.recv(1024).decode()
        # print(response)
        self.assertEqual(response.strip(), 'Moved to (0, 9)')

    def test_attack_monster(self):
        # print(7)
        self.client_cmd.do_attack('attack with sword')
        response = self.client_cmd.sct.recv(1024).decode()
        print(response)
        self.assertEqual(response.strip(), 'Attacked monster with sword. Damage 10 hp. monster now has 15 hp')


if __name__ == '__main__':
    unittest.main()
