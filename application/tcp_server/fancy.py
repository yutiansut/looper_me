from typing import Awaitable, Optional

from tornado.iostream import IOStream, StreamClosedError
from tornado.tcpserver import TCPServer

from application.logger import logger
from application.tcp_server.constant import AUTH_KEY, REPLY
from application.tcp_server.protocol import DataProtocol


class BaseServer(TCPServer):

    def handle_stream(
            self, stream: IOStream, address: tuple
    ) -> Optional[Awaitable[None]]:
        """ 处理流 """


class CoreServer(BaseServer):

    def connection_made(self, address, stream):
        """ 建立连接 """
        logger.info("connection made  from ", address)
        stream.write(REPLY['connect_reply'])

    def connection_lost(self, address: tuple, exception):
        """ 连接丢失 """
        logger.info("connection lost from ", address, "exception: ", exception)

    async def handler(self, type, content, stream):
        raise NotImplemented

    async def event_handler(self, data: DataProtocol, stream: IOStream, address:tuple):
        """ 处理不同情况的请求 """
        if not data.auth:
            # warnings.warn("数据来源无法进行校验")
            await stream.write(REPLY['unsupported_req'])
        else:
            await self.handler(data.type, data.content, stream, address)

    async def handle_stream(self, stream: IOStream, address: tuple):
        self.connection_made(address, stream)
        while True:
            try:
                data = await stream.read_until(AUTH_KEY)
                await self.event_handler(DataProtocol(data), stream, address)
            except StreamClosedError:
                self.connection_lost(address, StreamClosedError)
                break
