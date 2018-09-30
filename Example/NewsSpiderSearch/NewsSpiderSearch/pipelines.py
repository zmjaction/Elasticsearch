# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi
from DBUtils.PooledDB import PooledDB



class ElasticSearchPipeline(object):
    """通用的ELasticSearch存储方法"""

    def process_item(self, item, spider):
        item['FileList'] = str(item['FileList'])
        item.save_to_es()
        return item


class MysqlTwistedPipeline(object):
    """
    通用的数据库保存Pipeline
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        自定义组件或扩展很有用的方法: 这个方法名字固定, 是会被scrapy调用的。
        这里传入的cls是指当前的class
        """
        db_parms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        # 连接池ConnectionPool
        dbpool = adbapi.ConnectionPool("pymysql", **db_parms)

        # 此处相当于实例化pipeline, 要在init中接收。
        return cls(dbpool)

    # 处理item函数
    def process_item(self, item, spider):
        # 把要执行的sql放入连接池
        query = self.dbpool.runInteraction(self.insert_into, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql1 = 'insert ignore into tbl_NewsDetails201809(NewsID, NewsCategory, SourceCategory, NewsType, NewsTitle, NewsRawUrl, SourceName, AuthorName, InsertDate, NewsContent, NewsDate, NewsClickLike, NewsBad, NewsRead, NewsOffline)' \
               'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql2 = 'insert into tbl_NewsFileManager201809(FileID, FileType, FileDirectory, FileDirectoryCompress, FileDate, FileLength, FileUserID, Description, NewsID,image_url)' \
               'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        # 执行sql语句
        try:
            cursor.execute(sql1, (
                item['NewsID'], item["NewsCategory"], item["SourceCategory"], item["NewsType"], item["NewsTitle"],
                item["NewsRawUrl"], item["SourceName"], item["AuthorName"], item["InsertDate"], item["NewsContent"],
                item['NewsDate'], item['NewsClickLike'], item['NewsBad'], item['NewsRead'], item['NewsOffline']
            ))
            for dic in item['FileList']:
                cursor.execute(sql2, (
                    dic['FileID'], dic["FileType"], dic["FileDirectory"], dic["FileDirectoryCompress"],
                    dic["FileDate"],
                    dic["FileLength"], dic["FileUserID"], dic["Description"], dic["NewsID"], dic["image_url"]
                ))
        except Exception as e:
            print(e)
            print("执行sql语句失败")

    # 错误函数
    def handle_error(self, failure, item, spider):
        # #输出错误信息
        print(failure)








