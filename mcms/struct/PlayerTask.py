# _*_ coding: utf-8 _*_
import typing

class PlayerTask(object):
    '''玩家任务对象'''
    def __init__(self, name: str):
        self.name = name
        # 参数关键字
        self.keywords = []


    def __getitem__(self, item: str) -> typing.Any:
        if not hasattr(self, item):
            return None
        self.keywords.append(item)
        return getattr(self, item)


    def __setitem__(self, key: str, value: typing.Any) -> None:
        setattr(self, key, value)



if __name__ == "__main__":
    pass
