
from scrapy import cmdline


"""
调用execute函数执行scrapy命令，相当于在控制台cmd输入该命令
可以传递一个数组参数进来
"""

cmdline.execute("scrapy crawl sina".split())
