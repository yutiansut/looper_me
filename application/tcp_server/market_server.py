from application.tcp_server.buffer import Buffer
from application.tcp_server.constant import REPLY, REQ_TYPE
from application.tcp_server.fancy import CoreServer
from typing import Dict


class MarketServer(CoreServer):
    """ 交易服务器  --> maybe 没啥用 """

    def __init__(self):
        super().__init__()
        # 全局stream对象
        self.gloabl = {}
        self.buffers = {}

        # 缓冲区  ---> 这边应该自建一个块  而不是用一个list
        self.buffer = list()

    def connection_made(self, address, stream):
        self.gloabl[address[0]] = stream

    def connection_lost(self, address: tuple, exception):
        del self.gloabl[address[0]]

    def process_tick(self, tick):
        if tick.local_symbol not in self.buffers:
            self.buffers[tick.local_symbol] = Buffer(tick.local_symbol)
        self.buffers[tick.local_symbol].push(tick)

    async def process_data_req(self, local_symbol, type, start, end, stream):
        """ 处理数据请求 """
        pass

    async def subscribe(self, stream, address):
        # 发起订阅请求
        pass

    async def handler(self, type, content, stream):
        if type not in REQ_TYPE:
            pass
        await stream.write(REPLY['success'])
        # 行情服务器应该接受ctpbee客户端推送的tick

    async def election(self):
        pass

    async def broadcast(self, msg: bytes):
        """ 广播信息必须符合ctpbee的数据标准 """
        for stream in self.gloabl.values():
            """ 对所有连接进行推送数据 """
            await stream.write(msg)
