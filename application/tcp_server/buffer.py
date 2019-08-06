from time import time


class Buffer:

    def __init__(self, local_symbol, server, size=100):
        self.local_symbol = local_symbol
        self.size = size
        # 过期区域
        self.out_area = set()
        self.server = server
        # 当前正常区域
        self.cur_area = {}

    @property
    def window(self):
        cur = round(time() * 1000)
        return (cur - self.size, cur + self.size)

    def push(self, tick):
        if tick.feature in self.out_area:
            # 过滤过期数据
            return
        # 推送tick到源
        self.cur_area.setdefault(tick.feature, []).append(tick)


        # todo: 如果满足条件那么就 进行拜占庭选举

        # todo: 根据订阅列表进行推送  || 写入数据库

        # todo: 将特征值记录到过期区中去
