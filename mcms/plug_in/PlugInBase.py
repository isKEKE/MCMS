# _*_ coding: utf-8 _*_
import re
import threading
import queue
import typing
from mcms.struct import CoreItem
# from mcms.mcms import MinecraftManagementSystem


class PlugInBase(threading.Thread):
    '''插件编写基类'''
    # 插件名称
    name: str = None
    # 关键字
    keyword: str = None
    # 交互附属功能正则列表, (正则表达式，标记)
    inter_anci_func: typing.List[typing.Tuple[str, str, bool]] = None
    def __init__(self):
        super(PlugInBase, self).__init__()
        # 服务器核心
        self.core: 'MinecraftManagementSystem' = CoreItem.quote
        # 消息队列
        self.queue = queue.Queue()
        # 关闭信号
        self.flag = True
        # 玩家名称
        self.player = None
        # 标记
        self.sign = None
        # 参数
        self.args = None


    def go(self) -> None:
        pass


    def run(self) -> None:
        while True:
            if self.flag == False:
                break
            try:
                info = self.queue.get()
            except queue.Empty:
                pass
            else:
                if info == -1:
                    continue

                # 判断是否执行功能
                if not self.isExecute(info):
                    continue

                # 执行命令
                self.go()


    def isExecute(self, info: str) -> bool:
        '''判断是否执行, 且获得额外参数'''
        if self.keyword in info:
            self.sign = self.keyword
            info_list = info.split()
            # 玩家
            self.player = re.sub("[<>]", "", info_list.pop(0))
            info_list.pop(0)
            # 额外参数
            self.args = info_list
            return True

        # 正则列表
        if self.inter_anci_func is not None:
            for pattern, sign, flag in self.inter_anci_func:
                done = re.findall(pattern, info)
                if (done):
                    self.sign = sign
                    if flag == True:
                        self.player = done[0][0]
                        try:
                            self.args = done[0][1:]
                        except IndexError:
                            self.args = None
                        return True
                    else:
                        self.args = done[0]
                        return True


        return False


    def updatePlayerTasks(self, key: str, value: typing.Any) -> None:
        # 更新玩家任务
        task = self.core.player_tasks.find(self.player)
        if (task):
            task[key] = value
            return


    def stop(self) -> None:
        '''结束线程'''
        self.flag = False
        self.queue.put(-1)

