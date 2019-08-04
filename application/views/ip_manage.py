"""
ip_manage views ----->
后台管理 ip视图函数
"""
import tornado.web


class IpHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


