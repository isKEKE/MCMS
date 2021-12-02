# _*_ coding: utf-8 _*_
import threading
import queue
from mcms.struct import CoreItem
# from mcms.mcms import MinecraftManagementSystem
import sys


class ServerThreadHandler(threading.Thread):
    flag = True
    def __init__(self):
        super(ServerThreadHandler, self).__init__()
        # 获得核心对象
        self.core:'MinecraftManagementSystem' = CoreItem.quote
        # 消息队列集
        self.queue = queue.Queue()


    def run(self) -> None:
        while True:
            if ServerThreadHandler.flag == False:
                break
            # 线程队列对象，阻塞
            try:
                info = self.queue.get()
            except queue.Empty:
                pass
            else:
                if info == -1:
                    continue

                # 简单筛选一下
                info = info.split("[Server thread/INFO]:")[-1].strip()
                # 服务器信息添加到插件线程的消息队列中
                for key in self.core.plugin_item.keywords:
                    plugin_thread = self.core.plugin_item[key].get("thread")
                    if plugin_thread is not None:
                        plugin_thread.queue.put(info)


    def stop(self) -> None:
        '''关闭线程'''
        ServerThreadHandler.flag = False
        self.queue.put(-1)