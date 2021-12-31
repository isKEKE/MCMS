# _*_ coding: utf-8 _*_
import threading
import random
import time
from .FireworkCommand import FireworkCommand


class FireworkThread(threading.Thread):
    flag = False
    def __init__(self, server, x, y, z):
        super(FireworkThread, self).__init__()
        self.server = server
        self._fire = FireworkCommand(x, y, z)


    def run(self) -> None:
        while True:
            cmd = self._fire.command()
            self.server.execute(cmd)
            if FireworkThread.flag == False:
                break
            time.sleep(random.uniform(0, 0.5))