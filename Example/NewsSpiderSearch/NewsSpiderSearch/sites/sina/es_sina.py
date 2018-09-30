# -*- coding:utf-8 -*-
from elasticsearch_dsl import connections, Document, Keyword, Text, Integer, Date, Completion, analyzer
import datetime

connections.create_connection(hosts=["localhost"])

my_analyzer = analyzer('ik_smart')


class SinaArticleType(Document):
    # 文章类型，定义字段的类型
    suggest = Completion(analyzer=my_analyzer)

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


if __name__ == '__main__':
    SinaArticleType.init()  # 生成映射