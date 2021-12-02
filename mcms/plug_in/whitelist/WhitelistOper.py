# _*_ coding: utf-8 _*_
from mcms.plug_in.PlugInBase import PlugInBase
from .UUIDOper import UUIDOper


class WhitelistOper(PlugInBase):
    name = "whitelist"
    keyword = "!!whitelist"
    inter_anci_func = [
        ('''There are (\d+) whitelisted players: (.*)''', "list", False),
        ('''Disconnecting.*?id=(.*?),name=(.*?),''', "uuid", False)
    ]
    def __init__(self):
        super(WhitelistOper, self).__init__()
        self.uuid_oper = UUIDOper()


    def go(self) -> None:
        # !!whitelist
        if self.sign == self.keyword:
            if len(self.args) == 2:
                self.exec2()
            elif len(self.args) == 1:
                self.exec_()


        # There are 2 whitelisted players: isKEKE, Ann
        elif self.sign == "list":
            self.core.thread_item.server.say(
                msg=f"当前人数: {self.args[0]}; 名单列表: {self.args[-1]}",
                player=self.player
            )

            self.player = None


        elif self.sign == "uuid":
            uuid, name = self.args
            self.uuid_oper.read()
            self.uuid_oper.update(name, uuid)
            self.reload()


    def exec_(self) -> None:
        '''执行单参数命令'''
        if self.args[0] == "list":
            self.core.thread_item.server.execute("whitelist list")


    def exec2(self) -> None:
        '''执行多参数命令'''
        # 判断是否是OP
        if not self.player in self.core.operate_set:
            self.core.thread_item.server.say("Not Sufficient Permissions", self.player)
            return

        # 添加白名单
        cmd = "whitelist {} {}"
        if self.args[0] == "add":
            cmd = cmd.format("add", self.args[1])
        elif self.args[0] == "remove":
            cmd = cmd.format("remove", self.args[1])
        else:
            return

        self.core.thread_item.server.execute(cmd)
        self.core.thread_item.server.say("Success", self.player)
        self.reload()


    def reload(self) -> None:
        '''重载白名单'''
        self.core.thread_item.server.execute("whitelist reload")