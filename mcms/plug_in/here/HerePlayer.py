# _*_ coding: utf-8 _*_
from mcms.plug_in.PlugInBase import PlugInBase


class HerePlayer(PlugInBase):
    '''Here 高亮+打印坐标'''
    name = "here"
    keyword = "!!here"
    # isKEKE has the following entity data: [-84.23525149908026d, 90.0d, -224.49507251614153d]
    # isKEKE has the following entity data: "minecraft:overworld"
    inter_anci_func = [
        ("(.*?) has the following entity data: \[(.*?)\]", "pos", True),
        ('''(.*?) has the following entity data: "(.*?)"''', "world", True)
    ]
    def __init__(self):
        super(HerePlayer, self).__init__()


    def go(self) -> None:
        if self.sign is None:
            return

        if self.sign == self.keyword:
            # 坐标命令
            pos_cmd = f"data get entity {self.player} Pos"
            # 执行
            self.core.thread_item.server.execute(pos_cmd)


        elif self.sign == "pos":
            # 玩家坐标
            player_pos = [int(p.split(".")[0]) for p in self.args[0].split(", ")]
            self.updatePlayerTasks("pos", player_pos)
            # 世界指令
            world_cmd = f"data get entity {self.player} Dimension"
            # 执行命令
            self.core.thread_item.server.execute(world_cmd)

        elif self.sign == "world":
            # 玩家世界
            player_world = self.args[0]
            self.updatePlayerTasks("world", player_world)

        # 提交任务
        self.submit()


    def submit(self) -> None:
        '''提交任务'''
        task = self.core.player_tasks.find(self.player)
        if (task is not None):
            if task["pos"] and task["world"]:
                _player = task.name
                _world = task["world"].split(":")[-1]
                _pos = task["pos"]
                self.core.thread_item.server.say(
                    f"§f@Player>{_player} §c@World>{_world} §a@Pos>{_pos}"
                )
                # 高亮
                command = f"effect give {task.name} minecraft:glowing 15 0 true"
                self.core.thread_item.server.execute(command)

                task["pos"] = None
                task["world"] = None
        return