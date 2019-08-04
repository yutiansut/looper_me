import tornado.web

from application.views.ip_manage import IpHandler


def make_app():
    return tornado.web.Application([
        (r"/ip_manage", IpHandler),
    ])


