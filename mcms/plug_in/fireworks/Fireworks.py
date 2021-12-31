# _*_ coding: utf-8 _*_
from mcms.plug_in.PlugInBase import PlugInBase
from .FireworkThread import FireworkThread

class Fireworks(PlugInBase):
    name = "fire"
    keyword = "!!fire"
    def __init__(self):
        super(Fireworks, self).__init__()
        self.__pos = None
        self.__fire_thread = None


    def go(self) -> None:
        if not self.player in self.core.operate_set:
            self.core.thread_item.server.say("Not Sufficient Permissions", self.player)
            return
        if len(self.args) == 1:
            if self.args[0] == "on":
                self.on()
            elif self.args[0] == "off":
                self.off()
            elif self.args[0] == "show":
                self.show()

        elif len(self.args) == 4 and self.args[0] == "pos":
            self.pos()


    def on(self) -> None:
        '''打开'''
        if self.__pos is None:
            self.core.thread_item.server.say("请先设置<Pos>", self.player)
            return

        if self.__fire_thread is not None:
            self.core.thread_item.server.say("烟花线程已启动, 请先关闭.", self.player)
            return

        FireworkThread.flag = True
        self.__fire_thread = []
        for _ in range(4):
            thread = FireworkThread(self.core.thread_item.server, *self.__pos)
            thread.daemon = True
            thread.start()
            self.__fire_thread.append(thread)


    def off(self) -> None:
        '''关闭'''
        if self.__fire_thread is None:
            return
        FireworkThread.flag = False
        self.__fire_thread = None


    def pos(self) -> None:
        '''坐标'''
        try:
            x = int(self.args[1])
            y = int(self.args[2])
            z = int(self.args[3])
        except ValueError:
            self.core.thread_item.server.say(
                "请输入正确数据", self.player
            )
            return

        self.__pos = [x, y, z]


    def show(self) -> None:
        '''打印坐标'''
        self.core.thread_item.server.say(
            self.__pos or "Null", self.player
        )