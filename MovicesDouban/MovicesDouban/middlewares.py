# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html


from fake_useragent import UserAgent
import logging
import time
import hashlib
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from scrapy.http import HtmlResponse
from twisted.internet import defer
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.web.client import ResponseFailed
import json

logger = logging.getLogger(__name__)
class RandomUserAgentDownloaderMiddleware(object):
    '''随机切换UserAgent'''
    def process_request(self, request, spider):
        agent = UserAgent()
        agent_one = agent.random
        request.headers['User-Agent'] = agent_one
        logger.debug('正在使用的User-Agent：{}'.format(agent_one))

class ProxyDownloaderMiddleware(object):
    '''使用讯代理的动态转发，切换代理'''
    def __init__(self, secret, orderno):
        self.secret = secret
        self.orderno = orderno
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            secret=crawler.settings.get('SECRET'),
            orderno=crawler.settings.get('ORDERNO')
        )

    def process_request(self, request, spider):
        timestamp = str(int(time.time()))
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        string = string.encode()
        md5_string = hashlib.md5(string).hexdigest()
        sign = md5_string.upper()
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp
        request.meta['proxy'] = 'http://forward.xdaili.cn:80'
        request.headers["Proxy-Authorization"] = auth
        logger.debug('正在使用动态转发')


class RetryDownloaderMiddleware(object):
    """  如果response.text出现auth fail动态转发错误，
    或者response.text是{"msg":"检测到有异常请求从您的IP发出，请登录再试!","r":1}
    或者response.text是{"code":200,"msg":"The number of requests exceeds the limit"}
    重新将请求返回调度器中。
    """
    def __init__(self,settings):
        self.max_retry_times = settings.getint('RETRY_TIMES')

    @classmethod
    def from_crawler(cls, crawler ):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if 'auth fail' in response.text:
            # 如果出现动态转发的错误，将请求重新放入调度器中
            reason = 'swith_ip_error'
            return self._retry(self, request, reason, spider) or response

        try:
            if '检测到' in json.loads(response.text).get("msg"):
                # 如果response.text的内容为{"msg":"检测到有异常请求从您的IP发出，请登录再试!","r":1}
                # 则将请求重新放入调度器中
                reason = 'test_wrong_ip'
                return self._retry(self, request, reason, spider) or response
            elif 'exceeds'in json.loads(response.text).get("msg"):
                # 如果response.text的内容为{"code":200,"msg":"The number of requests exceeds the limit"}
                # 则将请求重新放入调度器中
                reason = 'The number of requests exceeds the limit'
                return self._retry(self, request, reason, spider) or response
        except:
            pass
        return response

    def _retry(self, request, reason, spider):
        # 重试次数加一
        retries = request.meta.get('retry_times', 0) + 1
        retry_times = self.max_retry_times
        # 调用数据收集器
        stats = spider.crawler.stats
        # 如果当前重试的次数小于最大请求次数
        if retries <= retry_times:
            logger.info("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': str(request.meta), 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            # retryreq为request对象
            retryreq = request.copy()
            # 将当前的重试次数写入meta中
            retryreq.meta['retry_times'] = retries
            # 将该request的dont_filter设置为True
            retryreq.dont_filter = True

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)

            return retryreq
        else:
            stats.inc_value('retry/max_reached')
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': str(request.meta), 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            with open(str(spider.name) + ".txt", "a") as f:
                f.write('{}got a error:reach the max retry times'.format(request.meta) + "\n")


class ExceptionDownloaderMiddleware(object):
    """捕获状态码为3、4、5开头的请求，以及出现异常的请求，构筑HtmlResponse(url='')，并返回"""
    ALL_EXCEPTIONS = (defer.TimeoutError,  DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, ResponseFailed,TCPTimedOutError,
                           IOError, TunnelError, TimeoutError)

    def __init__(self,settings):
        self.retry_enabled = settings.getbool('RETRY_ENABLED')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self,request,response,spider):

        if str(response.status).startswith('4') or str(response.status).startswith('5') or str(response.status).startswith('3'):
            with open(str(spider.name) + ".txt", "a") as f:
                f.write('{}got a response.status:{}'.format(request.meta, response.status) + "\n")
            response = HtmlResponse(url='')
            logger.info('{}got a response.status:{}'.format(request.meta, response.status))
            return response
        return response


    def process_exception(self, request, exception, spider):

        if isinstance(exception,self.ALL_EXCEPTIONS):
            with open(str(spider.name) + ".txt", "a") as f:
                f.write('{}got a exception:{}'.format(request.meta,exception) + "\n")
            logger.info('{}got a exception:{}'.format(request.meta, exception))
            response = HtmlResponse(url='')
            return response



