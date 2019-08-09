def cal_feature(tick) -> object:
    """ 通过传入tick进行计算特征后再返回新的tick"""
    # todo 计算身份特征
    setattr(tick, "ident_feature", None)

    # todo 计算数据特征
    setattr(tick, "data_feature", None)

    return tick
