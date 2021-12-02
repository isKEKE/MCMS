# _*_ coding: utf-8 _*_
import re
import threading
import queue
from mcms.struct import PlayerTask
from mcms.struct import CoreItem
# from mcms.mcms import MinecraftManagementSystem


class PlayerThreadHandler(threading.Thread):
    flag = True
    '''玩家线程处理器'''
    def __init__(self):
        super(PlayerThreadHandler, self).__init__()
        # 核心对象
        self.core = CoreItem.quote
        self.queue = queue.Queue()


    def run(self) -> None:
        while True:
            if PlayerThreadHandler.flag == False:
                break
            try:
                info =self.queue.get()
            except queue.Empty:
                pass
            else:
                if info == -1:
                    continue
                # 获得进入服务器的玩家
                match_obj = re.match(".*?: (.*?) joined the game", info)
                if match_obj:
                    player = match_obj.group(1)
                    # 玩家任务对象
                    if self.core.player_tasks.find(player) is None:
                        player_task = PlayerTask(player)
                        self.core.player_tasks.add(player_task)
                        continue
                    
                    
                match_obj = re.match(".*?: (.*?) left the game", info)
                if match_obj:
                    player = match_obj.group(1)
                    # 玩家任务对象，判断
                    task = self.core.player_tasks.find(player)
                    if task is not None:
                        self.core.player_tasks.remove(task)
                        continue


    def stop(self) -> None:
        '''关闭线程'''
        PlayerThreadHandler.flag = False
        self.queue.put(-1)
