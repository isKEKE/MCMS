# _*_ coding: utf-8 _*_
import os
import importlib
from mcms.struct import CoreItem

class Reload(object):
    '''重载插件'''
    def __init__(self, route: str):
        '''
        :param route: 插件路径
        :param plugInUnitItem: 插件功能集合数据结构
        '''
        self.route = route
        # 核心对象
        self.core = CoreItem.quote



    def read(self) -> None:
        '''读取插件'''
        # 当前路径
        pwd = os.path.abspath(self.route)
        # 插件路径
        plugin_path = os.path.join(pwd, "mcms", "plug_in")

        # 遍历
        for module_name in os.listdir(plugin_path):
            module_path = os.path.join(plugin_path, module_name)
            # 判断是否是目录
            if os.path.isdir(module_path) and module_name[:2] != "__":
                # 模块字典集
                module_dict = self.import_(f"mcms.plug_in.{module_name}")
                # 记录到数据结构中
                if module_dict is not None:
                    self.toMemory(module_dict)


    def import_(self, name:str) -> [dict, None]:
        '''导入模块'''
        module = importlib.import_module(name)
        try:
            config_ = module.config
        except AttributeError:
            pass
        else:
            return config_


    def toMemory(self, modules: dict) -> None:
        '''到内存记录'''
        name = modules.pop("name")
        self.core.plugin_item[name] = modules


if __name__ == "__main__":
    Reload("../plug_in").read()