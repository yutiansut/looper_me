from tornado.ioloop import IOLoop
import tornado.autoreload

from application import make_app
from application.tcp_server import md_server, trade_server

if __name__ == '__main__':
    md_server.listen(12572)
    md_server.start()

    trade_server.listen(12472)
    trade_server.start()

    app = make_app()
    app.listen(8888)
    IOLoop.instance().start()
