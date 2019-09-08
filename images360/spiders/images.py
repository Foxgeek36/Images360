# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urllib.parse import urlencode
import json
from images360.items import ImageItem


class ImagesSpider(Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']
    # https://image.so.com/z?ch=photography/ '摄影'分类链接

    def start_requests(self):
        # https://image.so.com/zjl?ch=photography&sn=30&listtype=new&temp=1 / 获取'摄影'类别数据的接口
        data = {'ch': 'photography', 'listtype': 'new'}
        base_url = 'https://image.so.com/zj?'
        # 'MAX_PAGE'为唯一变化的参数 +--
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            # attention +--
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            # -------------
            yield Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get('imageid')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('group_title')
            item['thumb'] = image.get('qhimg_thumb_url')
            yield item
