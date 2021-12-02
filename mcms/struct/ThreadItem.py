# _*_ coding: utf-8 _*_

class ThreadItem(object):
    # 服务器核心对象
    server: 'Server' = None

    # 服务器线程处理器
    server_handler: 'ServerThreadHandler' = None

    # 玩家线程处理器
    player_handler: 'PlayerThreadHandler' = None