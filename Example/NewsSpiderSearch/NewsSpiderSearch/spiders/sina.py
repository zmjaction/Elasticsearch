# -*- coding: utf-8 -*-
import scrapy
from NewsSpiderSearch.sites.sina.sinaitems import NewsItem
import json
# from NewsSpiderSearch.utils.file_model import File_mod

import uuid
import time, datetime
import re
import logging


class SinaSpider(scrapy.Spider):
    name = 'sina'

    baseURL = 'https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&page={}&encode=utf-8&callback=feedCardJsonpCallback&_=1538096279183'


    url_list = [baseURL]

    logging.getLogger("requests").setLevel(logging.WARNING
                                           )  # 将requests的日志级别设成WARNING
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='sinaline.log',
        filemode='w')

    def start_requests(self):
        for uri in self.url_list:
            for page in range(1, 10):
                yield scrapy.Request(uri.format(page), callback=self.parse_page)

    def parse_page(self, response):

        logging.debug('request url:------>' + response.url)

        response_url = response.url
        content = response.text[4:-12]
        results = content[content.index('(') + 1:-2]
        result = json.loads(results)
        if not result:
            return None
        for item in result['result']['data']:
            try:
                link = item.get('wapurl')
                SourceName = item.get('media_name')
                NewsDate = item.get('ctime')
                NewsTitle = item.get('title')
                yield scrapy.Request(link, meta={'SourceName': SourceName, 'NewsDate': NewsDate, 'NewsTitle': NewsTitle,
                                                 'response_url': response_url}, callback=self.parse_page_detaile)
            except:
                return None

    def parse_page_detaile(self, response):
        item = NewsItem()
        now_time = datetime.datetime.now().strftime('%Y%m')
        item['NewsID'] = now_time + '-' + str(uuid.uuid1())
        item['NewsCategory'] = '001.001'

        SourceCategory = response.xpath("//div[@class='path']/div[@class='channel-path']/a/text()").extract_first()
        if SourceCategory:
            item['SourceCategory'] = '新浪新闻-'+ response.xpath("//div[@class='path']/div[@class='channel-path']/a/text()").extract_first()
        else:
            item['SourceCategory'] = '新浪新闻-'+ '国内新闻'

        item['NewsType'] = 0

        NewsTitle = '新浪新闻-' + response.meta['NewsTitle']

        item['NewsTitle'] = NewsTitle

        item['NewsRawUrl'] = response.url

        item['SourceName'] = response.meta['SourceName']

        try:
            item['AuthorName'] = response.xpath(
                "//div[@class='left-wrapper']/div[@class='content-bd']/p[1]/text()").extract_first()
        except:
            item['AuthorName'] = 'None'

        item['InsertDate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item['NewsDate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        item['NewsClickLike'] = 'None'

        item['NewsBad'] = 'None'

        item['NewsRead'] = 'None'

        item['NewsOffline'] = 0
        logging.info('NewsTitle:' + NewsTitle + 'NewsRawUrl' + response.url)

        image_urls = response.xpath("//article[@class='art_box']//a//img/@src").extract()
        content = ''.join(response.xpath("//div[@class='article']/p | //p").extract())


        listFiles = []
        if image_urls:
            for image_url in image_urls:

                filemodel = {}
                filemodel['FileID'] = str(uuid.uuid1())
                filemodel['FileType'] = 0
                filemodel['FileDirectory'] = image_url
                filemodel['FileDirectoryCompress'] = image_url
                filemodel['FileDate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                filemodel['FileLength'] = None
                filemodel['FileUserID'] = None
                filemodel['Description'] = None
                filemodel['NewsID'] = item['NewsID']
                filemodel['image_url'] = image_url
                listFiles.append(filemodel)

        item['NewsContent'] = content
        item['FileList'] = listFiles

        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl sina".split())