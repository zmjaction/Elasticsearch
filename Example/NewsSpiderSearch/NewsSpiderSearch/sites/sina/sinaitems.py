# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from elasticsearch_dsl import connections

from NewsSpiderSearch.sites.sina.es_sina import SinaArticleType

from NewsSpiderSearch.utils.es_utils import generate_suggests

from NewsSpiderSearch.utils.common import real_time_count
# from NewsSpiderSearch.items import MysqlItem

es_sina = connections.create_connection(SinaArticleType)

SINA_NEWS = 0


class NewsItem(scrapy.Item):
    NewsID = scrapy.Field()
    NewsCategory = scrapy.Field()  # 资讯大类别
    SourceCategory = scrapy.Field()  # 资讯小类别
    NewsType = scrapy.Field()  # 资讯类型 0-文本，1-图文， 2-视频
    NewsTitle = scrapy.Field()  # 资讯标题

    NewsContent = scrapy.Field()  # 资讯正文内容

    NewsRawUrl = scrapy.Field()  # 文章的源地址

    SourceName = scrapy.Field()  # 资讯来源（网站名称）

    AuthorName = scrapy.Field()  # 作者名称
    InsertDate = scrapy.Field()  # 入库时间
    # image_url = scrapy.Field()  # 图片地址

    NewsDate = scrapy.Field()
    NewsClickLike = scrapy.Field()
    NewsBad = scrapy.Field()
    NewsRead = scrapy.Field()
    NewsOffline = scrapy.Field()
    FileList = scrapy.Field()

    def clean_data(self):
        """
        清洗数据
        :return:
        """
        pass

    def save_to_mysql(self):
        insert_sql = """
                   insert into tbl_NewsDetails201809(NewsID,NewsCategory, SourceCategory, NewsType,NewsTitle,NewsRawUrl,
                    SourceName, AuthorName,InsertDate, NewsContent, NewsDate,
                     NewsClickLike, NewsBad, NewsRead, NewsOffline
                     )
                   VALUES (%s, %s, %s, %s, %s
                   , %s, %s, %s, %s, %s,
                   %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE
                   NewsTitle=VALUES(NewsTitle)
               """
        # 如果存在则更新, 如果不存在则增加 ON DUPLICATE KEY UPDATE
        sql_params = (
            self['NewsID'], self["NewsCategory"], self["SourceCategory"], self["NewsType"], self["NewsTitle"],self["NewsRawUrl"],
            self["SourceName"], self["AuthorName"], self["InsertDate"], self["NewsContent"], self['NewsDate'],
            self["NewsClickLike"], self["NewsBad"], self["NewsRead"], self["NewsOffline"])

        insert_file_sql =  """
                   insert into tbl_NewsFileManager201809(FileID,FileType, FileDirectory, FileDirectoryCompress,FileDate,FileLength,
                    FileUserID, Description,NewsID, image_url
                     )
                   VALUES (%s, %s, %s, %s, %s
                   , %s, %s, %s, %s, %s,)
               """
        sql_params_file = (
            self['FileID'], self["FileType"], self["FileDirectory"], self["FileDirectoryCompress"], self["FileDate"],
            self["FileLength"], self["FileUserID"], self["Description"], self["NewsID"], self['image_url'])

        return insert_sql, sql_params, insert_file_sql, sql_params_file

    def save_to_es(self):

        article = SinaArticleType()
        article.NewsID = self['NewsID']
        article.NewsCategory = self['NewsCategory']
        article.SourceCategory = self['SourceCategory']
        article.NewsType = self['NewsType']
        article.NewsTitle = self['NewsTitle']
        article.NewsContent = self['NewsContent']
        article.NewsRawUrl = self['NewsRawUrl']
        article.SourceName = self['SourceName']
        article.InsertDate = self['InsertDate']
        article.NewsDate = self['NewsDate']
        article.FileList = self['FileList']

        # article.suggest = generate_suggests(es_sina, "sinanews", ((article.NewsTitle, 10)))

        real_time_count('sinanews_count', SINA_NEWS)

        article.save()

        return



    # def help_fields(self):
    #     for field in self.field_list:
    #         print(field, "= scrapy.Field()")
