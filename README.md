# 代码一：jdBooktop
京东图书爬虫

使用scrapy爬取京东图书销售信息。

爬取起始链接（ http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10001-1#comfort ）

每个商品的价格是通过Ajax动态加载的，如下所示：

获取价格的链接（ http://p.3.cn/prices/mgets?skuIds=J_(书本id) ）。书本id是从网页中获取到的。

### 爬取到的数据分析（根据前端显示样式进行分块处理）：

如图：

  - 1. 获取所有分类

![](https://github.com/TopcoderWuxie/photos/blob/master/jdBooktop1.jpg)

  - 2. 每个分类含有的标签（并不是每一个对应的分类中都含有）

![](https://github.com/TopcoderWuxie/photos/blob/master/jdBooktop2.jpg)

  - 3. 筛选条件（并不是每个对应的分类及标签都含有）

![](https://github.com/TopcoderWuxie/photos/blob/master/jdBooktop3.jpg)

  - 4. 商品列表（注意分页的获取）

![](https://github.com/TopcoderWuxie/photos/blob/master/jdBooktop4.jpg)

### 爬取过程中遇到错误

  - requests.packages.urllib3.connectionpool

requests请求过多，每次请求完毕以后没有关闭，使用requests.session()即可避免。

  - TypeError: 'unicode' object does not support item assignment

最后把所有非NoneType的字段都转化为str，使用unicode之前从没有遇到过这种错误，今天第一次，具体的解决方法还没找到。
