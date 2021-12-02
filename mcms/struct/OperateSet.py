# _*_ coding: utf-8 _*_
import os
import configparser

class OperateSet(set):
    def __init__(self, opPath: str, seq=()):
        super(OperateSet, self).__init__(seq)
        self.op_path = opPath


    def read(self) -> set:
        # 如果OP文件不存在，返回
        if not os.path.exists(self.op_path):
            return self

        config = configparser.ConfigParser()
        config.read(self.op_path)
        # OP数量
        try:
            op_length = int(config.get("OP", "LENGTH"))
        except ValueError:
            return self
        except configparser.NoSectionError:
            return self
        except configparser.NoOptionError:
            return self

        # 如果OP数量小于1，返回
        if int(op_length) < 1:
            return self

        # 遍历，获取名单
        for index in range(op_length):
            op_name = config.get("OP", str(index))
            self.add(op_name)

        return self


    def addOperate(self, op: str) -> None:
        '''添加管理员'''
        if op in self:
            return

        self.add(op)
        # 更新
        self.updateOperate()


    def rmOperate(self, op: str):
        '''删除管理员'''
        if not op in self:
            return
        # 集合删除
        self.remove(op)
        # 更新
        self.updateOperate()


    def updateOperate(self) -> None:
        '''更新玩家名单'''
        config = configparser.ConfigParser()
        config.add_section("OP")
        config.set("OP", "LENGTH", str(len(self)))

        for index, op_name in enumerate(self):
            config.set("OP", str(index), op_name)

        with open(self.op_path, "w") as fp:
            config.write(fp)




if __name__ == "__main__":
    pass


