from application.tcp_server.buffer import Buffer
from application.tcp_server.constant import REPLY, REQ_TYPE
from application.tcp_server.fancy import CoreServer
from application.model import db


class MarketServer(CoreServer):
    """ 交易服务器  --> maybe 没啥用 """

    def __init__(self):
        super().__init__()
        # 全局stream对象
        self.global_connection = {}

        self.tick_origin = set()
        self.blacklist = db.load_ip()

        self.buffers = {}
        self.subscribed_pool = {}

        # 缓冲区  ---> 这边应该自建一个块  而不是用一个list
        self.buffer = list()

    def connection_made(self, address, stream):
        if address[0] in self.blacklist:
            stream.close()
            return
        self.global_connection[address[0]] = stream
        print(f'{address} connected!')

    def connection_lost(self, address: tuple, exception):
        # del self.gloabl[address[0]]
        # del self.subscribed_pool[address]
        pass

    def process_tick(self, tick):
        if tick.local_symbol not in self.buffers:
            self.buffers[tick.local_symbol] = Buffer(tick.local_symbol, self)
        self.buffers[tick.local_symbol].push(tick)

    async def process_data_req(self, local_symbol, type, start, end, stream):
        """ 处理数据请求 """
        pass

    async def subscribe(self, stream, address):
        # 发起订阅请求
        self.subscribed_pool[address] = stream

    async def handler(self, type, content, stream, address):
        if type not in REQ_TYPE:
            pass
        if type == 'tick':
            self.tick_origin.add(address)
        await stream.write(REPLY['success'])
        # 行情服务器应该接受ctpbee客户端推送的tick
