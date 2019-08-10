"""
data views ----->
后台管理 data视图函数
"""
from datetime import datetime

from application.views import BaseHandle
from application.common import true_return, false_return
from application.tcp_server.mongo import MotorClient


async def filter(collection, start=None, end=None, download=False):
    data = []
    for colle in collection:
        if download:
            data.append(colle)
        motor_client = MotorClient(collection_name=colle)
        if start and end:
            cursor = motor_client.collection.find({"datetime": {'$gte': start, '$lte': end}}).sort('datetime')
            data.extend([document async for document in cursor if document.pop('_id', None) or 1])
            continue
        elif start:
            cursor = motor_client.collection.find({"datetime": {'$gte': start}}).sort('datetime')
            data.extend([document async for document in cursor if document.pop('_id', None) or 1])
            continue
        elif end:
            cursor = motor_client.collection.find({"datetime": {'$lte': end}}).sort('datetime')
            data.extend([document async for document in cursor if document.pop('_id', None) or 1])
            continue
        else:
            cursor = motor_client.collection.find().sort('datetime')
            data.extend([document async for document in cursor if document.pop('_id', None) or 1])

    return data


class DataHandler(BaseHandle):
    async def get(self):
        motor_client = MotorClient()
        collections = await motor_client.get_collections()
        data = []
        for i in collections:
            data.append({'name': i})
        self.write(true_return(data=data))

    async def post(self):
        code = self.get_argument('code')
        start = self.get_argument('start')
        end = self.get_argument('end')
        if not code:
            return
        if start:
            start = datetime.strptime(start, '%Y-%m-%d')
        if end:
            end = datetime.strptime(end, '%Y-%m-%d')
        res = await filter([code], start, end)
        self.write(true_return(data=res))


class DownloadFileHandler(BaseHandle):
    async def post(self):
        code = self.get_argument('code')
        start = self.get_argument('start', None)
        end = self.get_argument('end', None)
        if not code:
            return
        if start:
            start = datetime.strptime(start, '%Y-%m-%d')
        if end:
            end = datetime.strptime(end, '%Y-%m-%d')
        print(type(code),code)
        results = await filter([code], start, end, download=True)
        data_csv = ''
        filename = '数据下载_{}.csv'.format(code)
        for item in results:
            if isinstance(item, str): continue
            item['datetime'] = datetime.strftime(item['datetime'], '%Y-%m-%d %H:%M:%S')
            data_csv += '{},\r\n'.format(item, )
        self.set_header('Content-Type', 'application/csv')
        self.set_header('Content-Disposition', 'filename={}'.format(filename.encode('utf-8').decode('ISO-8859-1')))
        self.write(data_csv)
        self.finish()
