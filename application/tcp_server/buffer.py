from time import time
from application.global_variable import ORIGIN_NUMBER
from application.tcp_server.mongo import MotorClient
from ctpbee import dumps
from application.tcp_server.helper import cal_feature

class Buffer:

    def __init__(self, local_symbol, server, size=100):
        self.local_symbol = local_symbol
        self.size = size
        # 过期区域
        self.out_area = set()
        self.server = server
        # 当前正常区域
        self.cur_area = {}
        self.motor_client = MotorClient(collection_name=local_symbol)

    @property
    def window(self):
        cur = round(time() * 1000)
        return (cur - self.size, cur, cur + self.size)

    async def push(self, tick):
        tick = cal_feature(tick)
        if tick.ident_feature in self.out_area:
            # or not (self.window[0] < tick.datetime.timestamp() < self.window[1]):
            # 过滤过期数据
            return
        # 推送tick到源
        """
        self.cur_area = {
                        tick.ident_feature : {
                                                'all' : 5
                                                tick.data_feature1 : [tick1, tick2, tick3],
                                                tick.data_feature2 : [tick1, tick2],
                                                }
        }
        """
        self.cur_area.setdefault(tick.ident_feature, {'all': 0, tick.data_feature: []})[tick.data_feature].append(
            tick)
        self.cur_area[tick.ident_feature]['all'] += 1
        # 如果满足条件那么就 进行拜占庭选举 --->
        if self.cur_area[tick.ident_feature]['all'] >= ORIGIN_NUMBER:
            max_votes = 0
            res = ""
            for key, ticks in self.cur_area[tick.ident_feature].items():
                if key == 'all': continue
                if len(ticks) > max_votes:
                    max_votes = len(ticks)
                    res = ticks[0]
            # 根据订阅列表进行推送  || 写入数据库
            delattr(res, 'ident_feature')
            delattr(res, 'data_feature')
            # if res.symbol == 'zn1910':
            #     await self.motor_client.find()
            await self.motor_client.insert_one(res._to_dict())
            for addr, stream in self.server.subscribed_pool.items():
                await stream.write(res)
                self.cur_area.pop(tick.ident_feature, None)
            # 将特征值记录到过期区中去
            self.out_area.add(tick.ident_feature)