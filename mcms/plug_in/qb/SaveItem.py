# _*_ coding: utf-8 _*_

class SaveItem(object):
    '''存档目录'''
    def __init__(self):
        self.num_1: dict = None
        self.num_2: dict = None
        self.num_3: dict = None
        self.num_4: dict = None
        self.num_5: dict = None


if __name__ == "__main__":
    import pickle
    save = SaveItem()
    setattr(save, "num_1", {"index": "1"})
    print(save.num_1)


    # with open("save.pkl", "wb") as fp:
    #     obj = pickle.dump(save, fp)
    # # print(obj.num_1)

    save_ = pickle.load(open("save.pkl", "rb"))
    print(save_.num_1)