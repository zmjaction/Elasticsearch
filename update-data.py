# encoding: utf-8
__author__ = 'action'

"""
借鉴: https://cuiqingcai.com/6214.html

"""

from elasticsearch import Elasticsearch

es = Elasticsearch()

data = {
    'title': '美国留给伊拉克的是个烂摊子吗',
    'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
    'date': '2011-12-16'
}

# result = es.update(index='news', doc_type='politics', body=data, id=1)
# 数据更新调用update()方法即可

"""
result 字段为 updated，即表示更新成功，另外我们还注意到有一个字段 _version，这代表更新后的版本号数，
2 代表这是第二个版本，因为之前已经插入过一次数据，所以第一次插入的数据是版本 1，可以参见上例的运行结果，
这次更新之后版本号就变成了 2，以后每更新一次，版本号都会加 1

"""

result = es.index(index='news', doc_type='politics', body=data, id=1)
# index() 方法可以代替我们完成两个操作，如果数据不存在，那就执行插入操作，如果已经存在，那就执行更新操作，非常方便。
print(result)


