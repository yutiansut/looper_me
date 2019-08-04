from tornado.ioloop import IOLoop

from application import make_app
from application.tcp_server.market_server import MarketServer

if __name__ == '__main__':
    md_server = MarketServer()
    md_server.listen(12572)
    md_server.start()

    app = make_app()
    app.listen(8888)
    IOLoop.instance().start()
