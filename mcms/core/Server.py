# _*_ coding: utf-8 _*_
import sys
import threading
import time
from subprocess import Popen
from subprocess import PIPE
from mcms.struct import CoreItem


class Server(threading.Thread):
    flag = True
    def __init__(self, cmd:str, encoding: str):
        super(Server, self).__init__()
        self.cmd = cmd
        self.encoding = encoding
        # 核心对象
        self.core = CoreItem.quote

        # 管道对象
        self.pipe = None


    def run(self) -> None:
        while True:
            # 开始服务器
            self.started()
            # 获得服务器信息
            while True:
                info = self.pipe.stdout.readline().replace("\n", "")
                # 信息分配
                self.distribute(info)
                # 打印信息
                self.pprint(info)
                if not info:
                    break
            if Server.flag == False:
                break
            # 服务器重启，休息5s
            time.sleep(5)


    def started(self) -> None:
        '''开始服务器'''
        self.pipe = Popen(self.cmd, shell=True, stdout=PIPE,
                          stdin=PIPE, encoding=self.encoding)


    def execute(self, cmd: str) -> None:
        '''指令输入'''
        if not cmd:
            return
        # 重新编码
        cmd += "\n"
        try:
            cmd = cmd.encode("utf-8").decode(self.encoding)
        except UnicodeDecodeError:
            cmd = cmd.encode("cp936").decode(self.encoding)
        finally:
            self.pipe.stdin.write(cmd)
            self.pipe.stdin.flush()


    def stop(self) -> None:
        '''关闭服务器'''
        Server.flag = False
        self.execute("stop")


    def say(self, msg: str, player:str=None) -> None:
        '''讲话'''
        if player is not None:
            msg = f'''tellraw {player} {{"text": "§a[Root]: §7{msg}"}}'''
        else:
            msg = f'''tellraw @a {{"text": "§a[Root]: §7{msg}"}}'''

        self.execute(msg)


    def pprint(self, info: str) -> None:
        '''打印'''
        sys.stderr.write(f"{info}\n")


    def distribute(self, info: str) -> None:
        '''分配'''
        if "Server thread/INFO" in info:
            self.core.thread_item.server_handler.queue.put(info)
            self.core.thread_item.player_handler.queue.put(info)


if __name__ == "__main__":
    pass