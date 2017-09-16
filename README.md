# jdSpider
京东爬虫

### 预装软件
python3.5.2
Chrome 
python-selenium 
相关插件(chromedriver.exe)

通过京东搜索页面，用selenium模拟浏览器，实现对输入的商品进行搜索，爬取商品链接

京东搜索页面的初始url( ![](https://search.jd.com/) )

### 爬取过程中遇到的问题

- selenium.common.exceptions.StaleElementReferenceException

在爬取过程中发现在页面跳转的时候，总是会出现这个问题，后来找到了问题的具体原因，可以参见这个博客，讲解的很详细。

相关博客链接( ![](https://huilansame.github.io/huilansame.github.io/archivers/exceptions-StaleElementReferenceException) )

- 多线程中数据发生覆盖

开始设计的时候，是把所有的线程都放入一个线程队列中，等程序执行完以后再爬取每一页的商品url。但是发现后面的时候会出现数据覆盖，爬取的所有商品都变为了最后一个页面的商品url。于是对每个线程里面的driver加上了copy.deepcopy，可是这样会报错。所以最后就设计成线程只要创建了就去执行。

- 不符合爬取标准的商品

如图所示：

![](https://github.com/TopcoderWuxie/photos/blob/master/jdSearch1.jpg)

需要爬取的商品是左边的类型的，而右边这种不符合需要爬取的要求，因为跳转后里面显示的是店铺，而不是具体某个商品的基本信息。

### 为什么用selenium进行爬取

开始是用的requests，但是发现京东商品页面是先加载30个，然后往下翻页会动态加载出30个。当点击翻页的时候会发现，每一页的url中只能显示奇数页。所以之前提到的即为偶数页的内容。

如图所示：

![](https://github.com/TopcoderWuxie/photos/blob/master/jdSearch2.jpg)

![](https://github.com/TopcoderWuxie/photos/blob/master/jdSearch3.jpg)

观察图片可以发现，动态加载的url中的**show_items**指定的一堆id。其实这个就是上面30个商品的商品id，然后使用它们动态加载出下面的30个商品。

不过在尝试的时候，发现好多时候下面的30个商品都不能获取到，加载出来的url并不能解析出数据。

哎，还是技术不到家。

### 我用selenium的总结

- 超级难用。感觉selenium适合和多进程一块使用，每个进程中用selenium获取相同样式的页面。

在这个问题中也可以实现这种功能。可以执行**start_requests.py**中的**shop_name**为一个爬取列表，对每一个商品进行爬取的时候都开一个多进程，这种实现爬取速度会提高很多，而且可以实现爬取同时爬取多个商品。这种实现留给读者去尝试，肯定可以实现。

- selenium 真的不太适合爬取大型网站

很多人都说selenium并不太适合爬取大型网站，尝试了下，发现还真是这回事。确实不太合适，我用的是**Chrome**进行爬取的，因为用**PhantomJS**一直出现各种各样的问题。用PhantomJS应该会好点。

### 接下来要做的事

爬取商品id链接只是第一步，接下来会进行爬取商品页面的信息，以及每个商品的评论。后期还会有爬取**淘宝搜索页面**的爬虫,爬取的内容和京东相同

接下来会做的几件事（当爬虫写好，爬取的数据量达到以后）

- 分析买东西的人对不同价格的商品的偏好。更侧重于买哪一个价格区间的商品。

- 通过分析两个电商品牌的好评数，来总结下两大电商品牌的口碑对比。

- 爬取购买的裤子以及T恤等衣服来分析人们的身高比例。
	* 分男女装，用来分别统计男生和女生的身高比例
	* 通过两种方式判断身高：**1.**分别用每一类商品进行判断身高。**2.**把所有衣服进行合并，每一个衣服都用作一个特征值，用机器学习的算法去判断身高比例。

- 爬取罩杯的大小来分析中国的罩杯主要集中在哪一个类型。

- 对比昂贵商品的购买力，用来判断用户对于高价的商品更倾向于选择哪一个平台来购买。
