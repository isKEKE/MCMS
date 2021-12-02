# _*_ encodig: utf-8 _*_
from .PlayerTask import PlayerTask


class PlayerTaskSet(object):
    def __init__(self):
        self.__player_set = set()


    def add(self, element: PlayerTask) -> None:
        if not isinstance(element, PlayerTask):
            return
        # 添加
        self.__player_set.add(element)


    def find(self, name: str) -> PlayerTask:
        for task in self.__player_set:
            if task.name == name:
                return task

    def remove(self, element: PlayerTask) -> None:
        if not isinstance(element, PlayerTask):
            return

        self.__player_set.remove(element)

    def __str__(self) -> str:
        return str(self.__player_set)

    @property
    def set_(self) -> set:
        return self.__player_set


if __name__ == "__main__":
    pass