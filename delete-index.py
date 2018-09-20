# encoding: utf-8
__author__ = 'action'

"""
借鉴: https://cuiqingcai.com/6214.html

"""

from elasticsearch import Elasticsearch

es = Elasticsearch()

result = es.indices.delete(index='news', ignore=[400, 404])

print(result)

"""
这里也是使用了 ignore 参数，来忽略 Index 不存在而删除失败导致程序中断的问题
如果 Index 已经被删除，再执行删除,如果不添加ignore就会报错, 表示index不存在,删除失败, 状态码是400
由于我们添加了 ignore 参数，忽略了 400 状态码，因此程序正常执行输出 JSON 结果，而不是抛出异常

"""
