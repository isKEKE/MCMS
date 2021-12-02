# _*_ coding: utf-8 _*_
import json
import os

class UUIDOper(object):
    def __init__(self):
        self.json_path = "./whitelist.json"
        self.json_data = None


    def read(self) -> None:
        '''读取数据'''
        if not os.path.exists(self.json_path):
            self.json_data = None
            return

        with open(self.json_path, "r") as fp:
            self.json_data = json.loads(fp.read())


    def update(self, name: str, uuid: str) -> int:
        '''更新玩家uuid'''
        if type(self.json_data) != list:
            return -1

        for player in self.json_data:
            _name = player.get("name")
            if _name.lower() == name.lower():
                player["uuid"] = uuid
                player["name"] = name

        self.save()

        return 0



    def save(self) -> None:
        '''内存数据存储'''
        with open("whitelist.json", "w") as fp:
            json.dump(self.json_data, fp)


if __name__ == "__main__":
    uuid_oper = UUIDOper()
    pass