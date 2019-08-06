class DataProtocol:
    """ 解析请求 """

    def __init__(self, data):
        if isinstance(data, bytes):
            self.data = str(data, encoding="utf-8").replace("__d41d8cd98f00b204e9800998ecf8427e__", "")
        else:
            self.data = data.replace("__d41d8cd98f00b204e9800998ecf8427e__", "")
        self.type = None
        self.content = None
        self.auth = False
        self.key = None
        self.parse_result = False
        self._parse()
        self.auth_required()

    def _parse(self):
        """ 解析数据 """
        fancy = self.data.split("--")
        if len(fancy) != 3:
            return
        self.type = fancy[0]
        self.content = fancy[1]
        self.key = fancy[2]
        self.parse_result = True

    def auth_required(self):
        """ 装饰器 """
        if not self.parse_result:
            # 解析失败
            return
        self.auth = True

    def __repr__(self):
        return f"DataProtocol type: {self.type}, content: {self.content}"
