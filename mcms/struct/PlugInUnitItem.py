# _*_ coding: utf-8 _*_
import typing

class PlugInUnitItem(object):
    '''存储插件类对象的数据结构'''
    keywords = []
    def __getitem__(self, item: str) -> typing.Any:
        if not hasattr(self, item):
            return None
        return getattr(self, item)


    def __setitem__(self, key: str, value: typing.Any) -> None:
        setattr(self, key, value)
        PlugInUnitItem.keywords.append(key)


    def __str__(self):
        return str(PlugInUnitItem.keywords)






if __name__ == "__main__":
    # plug_in = PlugInUnitItem()
    # for i in plug_in:
    #     print(i)
    pass