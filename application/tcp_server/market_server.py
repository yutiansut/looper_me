from application.tcp_server.constant import REPLY
from application.tcp_server.fancy import CoreServer


class MarketServer(CoreServer):
    """ 行情服务器 """

    async def handler(self, type, content, stream):
        await stream.write(REPLY['success'])

        # 行情服务器应该接受ctpbee客户端推送的tick 
