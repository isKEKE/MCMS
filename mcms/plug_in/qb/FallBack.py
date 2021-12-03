# _*_ coding: utf-8 _*_
import os
import pickle
import time
from mcms.plug_in.PlugInBase import PlugInBase
from .SaveItem import SaveItem

class FallBack(PlugInBase):
    MAX_BYTE_SIZE = 50 * 1024 * 1024
    MAX_BYTE_BLOCK = 2 * 1024 * 1024
    name = "qb"
    keyword = "!!qb"
    def __init__(self):
        super(FallBack, self).__init__()
        # 存档名称
        self.save_name = None
        # 存档路径
        self.save_path = None
        # 缓存路径
        self.cache_path = None
        # 存档序列信息
        self.save_item = None
        # 存储序列信息所在路径
        self.save_item_path = "./config/save.pkl"
        # 读取
        self.readSaveName()
        self.readSaveItem()


    def go(self) -> None:
        if self.sign == self.keyword:
            if len(self.args) > 1:
                self.exec2()
            elif len(self.args) == 1:
                self.exec_()
            else:
                pass

        self.sign = None
        self.args = None
        self.player = None


    def exec_(self) -> None:
        '''单命令'''
        if self.args[0] == "list":
            self.list_()


    def exec2(self):
        '''OP相关'''
        if self.args[0] == "make":
            self.make()
        elif self.args[0] == "remove":
            self.remove()
        elif self.args[0] == "reload":
            # 判断是否是OP
            if not self.player in self.core.operate_set:
                self.core.thread_item.server.say("Not Sufficient Permissions", self.player)
                return
            self.reload()


    def make(self) -> None:
        '''make指令'''
        # 存档序号
        try:
            index = int(self.args[1])
            if index > 5 or index < 1:
               raise ValueError
        except ValueError:
            self.core.thread_item.server.say("Invalid Command")
            return

        # 备注
        try:
            remarks = self.args[2]
        except IndexError:
            remarks = None
        _temp_info = {
            "remarks": remarks,
            "player": self.player,
            "time": FallBack.now()
        }
        # 服务器存档刷新
        self.core.thread_item.server.execute("save-all flush")
        # 勿频繁，提示
        self.core.thread_item.server.say("请勿频繁, 保存中...")
        # 强等待5s
        time.sleep(5)
        # 添加记录
        setattr(self.save_item, f"num_{index}", _temp_info)
        # 更新本地
        self.updateSaveItem()
        # 设置路径
        self.setCachePath(index)
        # 复制目录数
        FallBack.copyTree(self.save_path, self.cache_path)
        self.core.thread_item.server.say("Success", self.player)


    def remove(self) -> None:
        '''remove指令'''
        index = self.getSaveIndex()
        if index is None:
            return

        setattr(self.save_item, f"num_{index}", None)
        self.core.thread_item.server.say("Success", self.player)
        # 更新
        self.updateSaveItem()


    def list_(self) -> None:
        '''list指令'''
        self.core.thread_item.server.say("<Save List>", self.player)
        for index in range(1, 6):
            save = getattr(self.save_item, f"num_{index}")
            if save is None:
                msg = f"index: {index}, Status: None"
                self.core.thread_item.server.say(msg)
                continue

            # 玩家
            player = save.get("player")
            # 备注
            remarks = save.get("remarks")
            # 时间
            time_ = save.get("time")
            # 信息
            msg = f"index: {index}, player: {player}, time: {time_},remarks: {remarks}"
            # 输出
            self.core.thread_item.server.say(msg)


    def reload(self) -> None:
        '''reload指令，回档'''
        index = self.getSaveIndex()
        if index is None:
            return

        # 存档信息对象
        save = getattr(self.save_item, f"num_{index}")
        if save is None:
            self.core.thread_item.server.say("Fallback error, save is null")
            return

        self.core.thread_item.server.say("§4Everyone, the server will be back in 5S.")
        count = 5
        while count > 0:
            self.core.thread_item.server.say(f"§4{count}")
            time.sleep(1)
            count -= 1
        # 服务器关闭
        self.core.stop_server()
        # 休息5s
        time.sleep(5)
        # 文档复制
        self.setCachePath(index)
        FallBack.copyTree(self.cache_path, self.save_path)
        # 休息5s
        time.sleep(5)
        # 重启服务器
        self.core.start_server()


    def getSaveIndex(self) -> int:
        '''获得存档序号'''
        try:
            index = int(self.args[1])
            if index > 5 or index < 1:
               raise ValueError
        except ValueError:
            self.core.thread_item.server.say("Invalid Command")
            return None
        else:
            return index



    def readSaveItem(self) -> None:
        '''读取存档序列信息对象'''
        if not os.path.exists(self.save_item_path):
            self.save_item = SaveItem()
            return

        # 读取
        with open(self.save_item_path, "rb") as fp:
            self.save_item = pickle.load(fp)


    def updateSaveItem(self) -> None:
        '''更新存档序列信息对象'''
        if self.save_item is None:
            return

        with open(self.save_item_path, "wb") as fp:
            pickle.dump(self.save_item, fp)


    def readSaveName(self) -> None:
        '''读取存档名称'''
        for line in open("./server.properties", "r"):
            if "level-name" in line:
                self.save_name = line.replace("\n", "").split("=")[-1]
                self.save_path = os.path.join("./", self.save_name)
                break
        else:
            self.save_name = None
            self.save_path = None
            self.cache_path = None


    def setCachePath(self, index: int) -> None:
        '''设置缓存路径'''
        self.cache_path = os.path.abspath(
            os.path.join("./cache", str(index))
        )


    @staticmethod
    def copyTree(fromDir: str, toDir: str) -> None:
        '''复制存档树'''
        # 遍历
        for fromName in os.listdir(fromDir):
            fromPath = os.path.abspath(
                os.path.join(fromDir, fromName)
            )
            toPath = os.path.abspath(
                os.path.join(toDir, fromName)
            )
            # 判断是否是文件夹
            if os.path.isdir(fromPath):
                # 创建目录
                if not os.path.exists(toPath):
                    os.makedirs(toPath)
                # 回调
                FallBack.copyTree(fromPath, toPath)
            else:
                FallBack.copyFile(fromPath, toPath)


    @staticmethod
    def copyFile(fromFile: str, toFile: str) -> None:
        '''复制文件'''
        if fromFile.endswith("session.lock"):
            return

        # 当文件大小大于50M，进行块读取
        if os.path.getsize(fromFile) > FallBack.MAX_BYTE_SIZE:
            with open(toFile, "wb") as toFP:
                fromFP = open(fromFile, "rb")
                while True:
                    try:
                        chunk = fromFP.read(FallBack.MAX_BYTE_BLOCK)
                    except PermissionError:
                        break
                    if not chunk:
                        break
                    # 写入
                    toFP.write(chunk)
                fromFP.close()
        else:
            try:
                open(toFile, "wb").write(
                    open(fromFile, "rb").read()
                )
            except PermissionError:
                pass

    @staticmethod
    def now() -> str:
        return time.strftime("%d-%m/%Y %H:%M:%S", time.localtime())


if __name__ == "__main__":
    pass
