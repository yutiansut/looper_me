from time import time
from application.global_variable import ORIGIN_NUMBER



class Buffer:

    def __init__(self, local_symbol, server, size=100):
        self.local_symbol = local_symbol
        self.size = size
        # 过期区域
        self.out_area = set()
        self.server = server
        # 当前正常区域
        self.cur_area = {}
        self.counter = {}

    @property
    def window(self):
        cur = round(time() * 1000)
        return (cur - self.size, cur, cur + self.size)

    async def push(self, tick):
        if tick.feature in self.out_area or not (self.window[0] < tick.timestamp < self.window[1]):
            # 过滤过期数据
            # todo: 将特征值记录到过期区中去
            self.out_area.add(tick.identity_feature)
            return
        # 推送tick到源
        """
        self.cur_area = {
                        tick.identity_feature : {
                                                'all' : 5
                                                tick.data_feature1 : [tick1, tick2, tick3],
                                                tick.data_feature2 : [tick1, tick2],
                                                }
        }
        """
        self.cur_area.setdefault(tick.identity_feature, {'all': 0, tick.data_feature: []})[tick.data_feature].append(
            tick)
        self.cur_area[tick.identity_feature]['all'] += 1
        # todo: 如果满足条件那么就 进行拜占庭选举 --->
        if self.cur_area[tick.identity_feature]['all'] >= ORIGIN_NUMBER:
            max_votes = 0
            res = ""
            for ticks in self.cur_area[tick.identity_feature].values():
                if len(ticks) > max_votes:
                    max_votes = len(ticks)
                    res = ticks[0]
            # todo: 根据订阅列表进行推送  || 写入数据库
            for addr, stream in self.server.subscribed_pool.items():
                # await stream.write(res)
                self.cur_area.clear()


