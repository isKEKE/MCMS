# _*_ coding: utf-8 _*_
from mcms.plug_in.PlugInBase import PlugInBase


class OperateOper(PlugInBase):
    name = "op"
    keyword = "!!op"
    def __init__(self):
        super(OperateOper, self).__init__()


    def go(self) -> None:
        if not self.player in self.core.operate_set:
            self.core.thread_item.server.say("Not Sufficient Permissions", self.player)
            return

        if len(self.args) > 1:
            # 执行多参数功能
            self.exec2()
            self.core.thread_item.server.say("Success", self.player)
            
        elif len(self.args) == 1:
            # 执行单参数功能
            self.exec_()


    def exec_(self):
        '''单参数'''
        if self.args[0] == "list":
            self.core.thread_item.server.say(
                self.core.operate_set, self.player)


    def exec2(self) -> None:
        '''多参数'''
        if self.args[0] == "add":
            self.core.operate_set.addOperate(self.args[1])
        elif self.args[0] == "remove":
            self.core.operate_set.rmOperate(self.args[1])
