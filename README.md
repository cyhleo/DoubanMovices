# DoubanMovices
该项目用来抓取豆瓣电影中记录的2015年到2019年的所有电影信息，共抓取了37527部电影数据。

# 部分结果展示
![](https://github.com/cyhleo/DoubanMovices/blob/master/MovicesDouban/image/result.png)

# 项目说明

豆瓣网站通过检测ip值和请求头来反爬，一旦检测异常，通过以下措施来反爬虫    
1. 抛出TCPTimedOutError、TimeoutError、TunnelError。
2. 302 跳转到其他页面。
3. 发送状态码为200的响应”{‘msg’:’检测到有异常请求从你的IP 发出，请登录使用豆瓣。’,’r’:1}”
4. 发送状态码为200的响应”{‘msg’:’检测到有异常请求从你的IP 发出，请登录使用豆瓣。’,’r’:1}”

为了解决第一种情况，在settings中设置RETRY_ENABLED=True，开启下载器中间件'scrapy.downloadermiddlewares.retry.RetryMiddleware'，设置最大重试次数=7。

为了解决第二种情况，将302状态码添加到RETRY_HTTP_CODES列表中。当响应的状态码为302时，将请求重新返回调度器中。设置REDIRECT_ENABLED = False，禁用'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware'下载器中间件。

为了解决第三和第四种情况，编写‘MovicesDouban.middlewares.RetryDownloaderMiddleware
’下载器中间件，将请求重新放入调度器中。

此外，该项目中还编辑了ExceptionDownloaderMiddleware类，该类为最后执行的下载器中间件类（下载器下载好的response被引擎调度到spider的过程），捕获状态码为3、4、5开头的请求，以及出现异常的请求，构筑HtmlResponse(url='')，并将其返回。
 
# 告示     
本代码仅作学习交流，切勿用于商业用途。如涉及侵权，请告知，会尽快删除。
