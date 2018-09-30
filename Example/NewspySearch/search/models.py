from django.db import models

# Create your models here.
from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

connections.create_connection(hosts=["localhost"])

my_analyzer = analyzer('ik_smart')


class SinaIndex(Document):
    """新浪新闻文章类型"""
    NewsID = Keyword()
    NewsCategory = Text(analyzer="ik_max_word")  # text类型可以分词
    SourceCategory = Keyword()  # 不能分词，会以字符串保存
    NewsType = Integer()
    NewsTitle = Text(analyzer="ik_max_word")
    NewsContent = Text(analyzer="ik_max_word")
    tageword = Text(analyzer="ik_max_word")
    contentTags = Text(analyzer="ik_max_word")
    NewsRawUrl = Keyword()
    SourceName = Keyword()
    InsertDate = Date()
    NewsDate = Date()
    FileList = Keyword()


    class Index:
        name = 'sinanews'


