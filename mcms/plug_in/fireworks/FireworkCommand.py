# _*_ coding: utf-8 _*_
import random
import json
import pickle


class FireworkCommand(object):
    colors = pickle.load(open("colors.pkl", "rb"))
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


    def pos(self) -> str:
        '''随机坐标'''
        _x = self.x + random.randint(-64, 64)
        _y = self.y + random.randint(10, 30)
        _z = self.z + random.randint(-64, 64)
        return f"{_x} {_y} {_z}"


    def explosion(self) -> str:
        '''单爆炸'''
        return json.dumps({
            "Flicker": random.randint(0, 1),
            "Type": random.randint(0, 4),
            "Colors": -1,
            "FadeColors": -2
        }).replace(
            "-1", f"[I;{random.choice(FireworkCommand.colors)}]"
        ).replace(
            "-2", f"[I;{random.choice(FireworkCommand.colors)}]"
        )



    def explosions(self) -> str:
        explosions_str = "[{}]"
        explosion_list = []
        for _ in range(random.randint(4, 6)):
            explosion_list.append(self.explosion())
        explosions_str = explosions_str.format(
            ", ".join(explosion_list)
        )
        return explosions_str


    def tag(self) -> str:
        tag_dict = {
            "Fireworks": {
                "Explosions": -1,
                "Flight": random.randint(1, 3)
            }
        }
        tag = json.dumps(tag_dict)
        tag = tag.replace("-1",  self.explosions())
        return tag


    def nat(self) -> str:
        nat_dict = {
            "LifeTime": random.randint(10, 30),
            "FireworksItem": {
                "id": "firework_rocket",
                "Count": 1,
                "tag": -1,
            }
        }
        return json.dumps(nat_dict).replace("-1", self.tag())


    def command(self) -> str:
        return f"summon firework_rocket {self.pos()} {self.nat()}"


if __name__ == "__main__":
    pass