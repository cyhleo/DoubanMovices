# -*- coding: utf-8 -*-



BOT_NAME = 'MovicesDouban'

SPIDER_MODULES = ['MovicesDouban.spiders']
NEWSPIDER_MODULE = 'MovicesDouban.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 在爬虫结束的时候不清空请求队列和去重指纹队列
SCHEDULER_PERSIST = True

# 在爬虫开始的时候不清空请求队列
SCHEDULER_FLUSH_ON_START = False
# 启用scrapy_redis内置的调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
#  启动scrapy_redis内置的请求去重类
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# 启用scrapy_redis内置的优先级队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'

#请求队列和去重指纹队列存储使用的redis数据库info
REDIS_HOST = ''
REDIS_PORT = ''
REDIS_PASSWORD = ''


# 设置最小的下载延迟时间
DOWNLOAD_DELAY = ''

# 开启自动限速设置
AUTOTHROTTLE_ENABLED = True

# The initial download delay
AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60

# 发送到每一个服务器的并行请求数量
AUTOTHROTTLE_TARGET_CONCURRENCY = ''

# 设置并发数
CONCURRENT_REQUESTS = ''
CONCURRENT_REQUESTS_PER_DOMAIN = ''
CONCURRENT_REQUESTS_PER_IP = ''

# 禁用cookies
COOKIES_ENABLED = False


# 设置请求头
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Accept-Language':'zh-CN,zh;q=0.9',
  'Connection': 'keep-alive',
  'Host': 'movie.douban.com',
  'Referer': 'https://movie.douban.com/tag/'
}

# 关闭telnet
TELNETCONSOLE_ENABLED = False

# 讯代理动态转发
SECRET = ''
ORDERNO = ''

# 下载器中间件设置
DOWNLOADER_MIDDLEWARES = {
   'MovicesDouban.middlewares.RandomUserAgentDownloaderMiddleware': 533,
   'MovicesDouban.middlewares.ProxyDownloaderMiddleware': 543,
   'MovicesDouban.middlewares.RetryDownloaderMiddleware': 200,
   'MovicesDouban.middlewares.ExceptionDownloaderMiddleware': 90,
}

# 扩展设置
EXTENSIONS = {
   'MovicesDouban.latencies.Latencies': 500,
}

# 设置测试吞吐量和延迟的时间间隔
LATENCIES_INTERVAL = 5

# item pipeline设置
ITEM_PIPELINES = {
   'MovicesDouban.pipelines.MongoPipeline': 300,
}

# 数据持久化，mongodb设置
MONGO_URI = ''
MONGO_DB = ''

# 开启日志
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'

#logger输出格式设置
LOG_FORMATTER = 'scrapy.logformatter.LogFormatter'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# 如果为True，则进程的所有标准输出（和错误）将重定向到日志。 例如，如果您打印（'hello'）它将出现在Scrapy日志中。
LOG_STDOUT = False

# 显示的日志最低级别
LOG_LEVEL = 'INFO'

import datetime
t = datetime.datetime.now()
log_file_path = './log_{}_{}_{}_{}.log'.format(t.month,t.day,t.hour,t.minute)
# log磁盘保存地址
LOG_FILE = log_file_path


RETRY_ENABLED = True
# 最大重试次数
RETRY_TIMES = 7  # initial response + 7 retries = 8 requests
# 需要重试的响应重试状态码
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 302]

# 关闭重定向中间件
REDIRECT_ENABLED = False