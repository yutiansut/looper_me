from application.tcp_server.constant import REPLY
from application.tcp_server.fancy import CoreServer


class MarketServer(CoreServer):
    """ 交易服务器  --> maybe 没啥用 """

    def __init__(self):
        super().__init__()
        # 全局stream对象
        self.gloabl = {}

        # 缓冲区  ---> 这边应该自建一个块  而不是用一个list
        self.buffer = list()

    def connection_made(self, address, stream):
        self.gloabl[address[0]] = stream

    def connection_lost(self, address: tuple, exception):
        del self.gloabl[address[0]]

    async def handler(self, type, content, stream):
        await stream.write(REPLY['success'])
        # 行情服务器应该接受ctpbee客户端推送的tick

    async def election(self):
        pass

    async def broadcast(self, msg: bytes):
        """ 广播信息必须符合ctpbee的数据标准 """
        for stream in self.gloabl.values():
            """ 对所有连接进行推送数据 """
            await stream.write(msg)
