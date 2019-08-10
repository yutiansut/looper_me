# coding:utf-8
AUTH_KEY = b"__d41d8cd98f00b204e9800998ecf8427e__"

REPLY = {
    "unsupported_req": bytes('{"result": "error", "message":"非法请求, 无法校验成功"}', encoding="utf-8"),
    "unsupported_type": bytes('{"result": "error", "message":"不被支持的请求类型"}', encoding="utf-8"),
    "success": bytes('{"result": "success", "message":"请求成功"}', encoding="utf-8"),
    "failed": bytes('{"result": "failed", "message":"请求失败"}', encoding="utf-8"),
    "connect_reply": bytes('{"result": "success", message:"连接建立成功"}', encoding="utf-8")
}

"""
type: data_req
content {
        "des":local_symbol,
        "start": start_date,
        "end": end_date,
        } 

"""
"""
type: subscribe
content: {
            "des":local_symbol,
        }
 
"""

"""
type: tick
content:{
    "data":tick
}
"""

#

REQ_TICK = "tick"
REQ_SUB = "subscribe"
REQ_DATA = "data_req"


REQ_TYPE =[REQ_DATA, REQ_SUB, REQ_TICK]


# 解析函数
