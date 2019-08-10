from hashlib import md5


def cal_feature(tick) -> object:
    """ 通过传入tick进行计算特征后再返回新的tick"""
    # todo 计算身份特征
    setattr(tick, "ident_feature", str(tick.local_symbol) + str(tick.datetime.timestamp()))

    # todo 计算数据特征
    attrs = ['volume', 'last_price', 'limit_up', 'limit_down', 'open_price', 'high_price', 'low_price', 'pre_close',
             'open_interest', 'bid_price_1', 'ask_price_1', 'bid_volume_1', 'ask_volume_1']
    data_feature = ''
    for i in attrs:
        md5_val = md5(str(getattr(tick, i)).encode()).hexdigest()
        data_feature += md5_val[0] + md5_val[-1]
    setattr(tick, "data_feature", data_feature)
    return tick
