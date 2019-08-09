import json


def true_return(msg='', data=''):
    return json.dumps({
        'success': True,
        'msg': msg,
        'data': data
    })


def false_return(msg='', data=''):
    return json.dumps({
        'success': False,
        'msg': msg,
        'data': data
    })
