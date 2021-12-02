# _*_ coding: utf-8 _*_
from .core import Server
from .core import Reload
from .struct import ThreadItem
from .struct import PlugInUnitItem
from .struct import PlayerTaskSet
from .struct import OperateSet
from .struct import CoreItem
from .handler.server_thread import ServerThreadHandler
from .handler.server_thread import PlayerThreadHandler

from config import MC_RUN_COMMAND
from config import ENCODE
from config import OP_PATH


class MinecraftManagementSystem(object):
    def __init__(self):
        # 核心对象引用
        CoreItem.quote = self
        # 存储线程集
        self.thread_item = ThreadItem()
        # 插件功能集
        self.plugin_item = PlugInUnitItem()
        # 玩家任务集合
        self.player_tasks = PlayerTaskSet()
        # 管理员集合, 并加载OP名单
        self.operate_set = OperateSet(OP_PATH).read()
        # 重载对象
        self.reload = Reload(".")
        self.reload.read()
        # 初始化线程
        self.initThreads()


    def initThreads(self) -> None:
        '''初始化线程'''
        # 服务器线程处理器
        self.thread_item.server_handler = ServerThreadHandler()

        # 玩家线程处理器
        self.thread_item.player_handler = PlayerThreadHandler()



    def userPut(self) -> None:
        '''用户输入'''
        while True:
            reply = input("[User]: ")
            if reply.lower() == "start":
                self.start_server()
            elif reply.lower() == "stop":
                self.stop_server()
            elif reply.lower() == "quit":
                self.stop_server()
                self.stop_thread()
                break
            else:
                if self.thread_item.server is not None:
                    self.thread_item.server.execute(reply)


    def start_server(self) -> None:
        '''开启服务器'''
        # 服务器核心线程
        Server.flag = True
        self.thread_item.server = Server(
            MC_RUN_COMMAND, ENCODE
        )

        self.thread_item.server.start()


    def stop_server(self) -> None:
        '''关闭服务器'''
        if self.thread_item.server is None:
            return
        self.thread_item.server.stop()
        self.thread_item.server = None


    def start_thread(self) -> None:
        # 服务器线程信息处理
        self.thread_item.server_handler.start()
        # 玩家处理线程
        self.thread_item.player_handler.start()
        # 开始插件线程
        for key in self.plugin_item.keywords:
            cls = self.plugin_item[key].get("class")
            # 线程实例化
            plugin_thread =  cls()
            # 开始线程
            plugin_thread.start()
            # 记录
            self.plugin_item[key].update(
                {"thread": plugin_thread}
            )


    def stop_thread(self) -> None:
        # 服务器线程关闭
        self.thread_item.player_handler.stop()
        self.thread_item.server_handler.stop()

        # 插件线程关闭
        for key in self.plugin_item.keywords:
            thread = self.plugin_item[key].get("thread")
            if thread is not None:
                thread.stop()


    def go(self) -> None:
        '''开始'''
        self.start_thread()
        # 主线程，用户输入
        self.userPut()


if __name__ == "__main__":
    MinecraftManagementSystem().go()