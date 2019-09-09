# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import pymysql
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline  # scrapy自带的下载图片的操作类/ 查看官方文档及源码


class MongoPipeline(object):
    '''
    存储数据至mongodb中
    '''
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):  # 需要参数注入的类方法
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def process_item(self, item, spider):
        name = item.collection  # ImageItem内所设置
        self.db[name].insert(dict(item))  # attention +--
        return item
    
    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline():
    '''
    将数据存储至mysql
    '''
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )
    
    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()
    
    def close_spider(self, spider):
        self.db.close()
    
    def process_item(self, item, spider):
        print(item['title'])
        data = dict(item)
        # attention +--
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        # attetion +--
        self.cursor.execute(sql, tuple(data.values()))  # tuple(data.values())=(1, 2, 3)
        # -------------
        self.db.commit()
        return item


class ImagePipeline(ImagesPipeline):
    '''
    下载图片保存至本地/ 为最先执行顺序->先对下载结果做判断处理再依次将数据存储至mongodb&mysql中
    -此类为继承之后做重写 +--
    '''
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    # attention +--
    def item_completed(self, results, item, info):
        '''
        对图片下载结果做判断/ 注意参数results
        '''
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item
    
    def get_media_requests(self, item, info):  # 注意该函数的作用/ ->承接处理上一个函数下载失败的item?
        yield Request(item['url'])
