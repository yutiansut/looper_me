from functools import lru_cache
from hashlib import md5


@lru_cache(maxsize=100000)
def cal_md(string):
    return md5(string.encode()).hexdigest()


def cal_feature(tick) -> object:
    """ 通过传入tick进行计算特征后再返回新的tick"""
    setattr(tick, "ident_feature", str(tick.local_symbol) + str(tick.datetime.timestamp()))

    attrs = ['volume', 'last_price', 'limit_up', 'limit_down', 'open_price', 'high_price', 'low_price', 'pre_close',
             'open_interest', 'bid_price_1', 'ask_price_1', 'bid_volume_1', 'ask_volume_1']
    data_feature = ''
    for i in attrs:
        value = str(getattr(tick, i))
        md5_val = cal_md(value)
        data_feature += md5_val[0] + md5_val[-1]
    setattr(tick, "data_feature", data_feature)
    return tick
