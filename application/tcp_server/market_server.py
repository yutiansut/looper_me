from application.tcp_server.constant import REPLY
from application.tcp_server.fancy import CoreServer


class MarketServer(CoreServer):
    """ 交易服务器  --> maybe 没啥用 """

    async def handler(self, type, content, stream):
        await stream.write(REPLY['success'])

        # 在线模拟成交 ----> fancy
        # 行情服务器应该接受ctpbee客户端推送的tick
