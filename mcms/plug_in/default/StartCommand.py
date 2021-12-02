# _*_ coding: utf-8 _*_
import re
from mcms.plug_in.PlugInBase import PlugInBase

class StartCommand(PlugInBase):
    name = "default"
    keyword = "!!defaults"
    inter_anci_func = [
        (re.compile('''.*?Time elapsed: \d+ ms'''),
         "cmd", False)
    ]
    # 服务器启动指令
    start_commands = [
        "carpet viewDistance 10",
        "carpet xpNoCooldown true",
        "carpet combineXPOrbs true",
        "carpet flippinCactus true",
        "carpet antiCheatDisabled true",
        "carpet onePlayerSleeping true",
        "carpet customMOTD _",
        "carpet fastRedstoneDust true",
        "carpet lagFreeSpawning true",
        "carpet commandPlayer true",           # 允许非OP玩家使用player指令
        "carpet language zh_cn",
        "gamerule logAdminCommands false",
        "gamerule sendCommandFeedback false",
        "spawn mobcaps set 40"
    ]
    def __init__(self):
        super(StartCommand, self).__init__()


    def go(self) -> None:
        if self.sign == "cmd":
            for cmd in StartCommand.start_commands:
                self.core.thread_item.server.execute(cmd)