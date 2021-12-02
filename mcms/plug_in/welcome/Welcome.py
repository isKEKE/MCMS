# _*_ coding: utf-8 _*_
import re
import time
from mcms.plug_in.PlugInBase import PlugInBase


class Welcome(PlugInBase):
    '''玩家欢迎标题'''
    name = "welcome"
    keyword = "!!welcome"
    inter_anci_func = [
        ('''(.*?) joined the game''', "join", False)
    ]
    def __init__(self):
        super(Welcome, self).__init__()


    def go(self) -> None:
        if self.sign == "join":
            time.sleep(1)
            player = self.args
            for cmd in [
                f"title {player} times 15 30 15",
                f'''title {player} subtitle {{"text": "浪漫是红石与建筑", "color": "#FFFF66"}}''',
                f'''title {player} title {{"text":"Welcome To Server", "color": "#FF6666"}}'''
            ]:
                self.core.thread_item.server.execute(cmd)
