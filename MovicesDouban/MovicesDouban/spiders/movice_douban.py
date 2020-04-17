# -*- coding: utf-8 -*-
import scrapy
import json
from MovicesDouban.items import DoubanItem

class MoviceDoubanSpider(scrapy.Spider):
    name = 'movice_douban'
    allowed_domains = ['douban.com']

    base_urls = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=电影&start={}&genres={}&year_range={},{}'
    #    base_urls = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=2000&year_range=2010,2010'
    genres_list = ['剧情','喜剧','动作','爱情','科幻','动画',
                   '悬疑','惊悚','恐怖','犯罪','同性','音乐',
                   '歌舞','传记','历史','战争','西部','奇幻',
                   '冒险','灾难','武侠','情色']
    def start_requests(self):
        # for year in range(2015, 2019):

        # 2019年已经抓取完
        # 这次没有出现状态码200的{"msg":"检测到有异常请求从您的IP发出，请登录再试!","r":1}
        # 因为把最大的重试次数大小调大，所以其他的状态码，和异常，都通过scrapy 重试中间件解决了。
        # 15-18年的电影还得再爬一次

        for year in range(2015, 2019):
            for genres in self.genres_list:
                    yield scrapy.Request(self.base_urls.format(0,genres,year,year), meta={'start': 0,'genres':genres,'year':year})



    def parse(self, response):

        self.logger.info('response.text:{}{}'.format(type(response.text),response.text))
        try:
            self.logger.info(json.loads(response.text).get("msg"))
        except:
            pass
        if response and response.url:
            # print('json.loads(response.text):{}'.format(json.loads(response.text)))
            films_list = json.loads(response.text).get('data')
            self.logger.debug('films_list:{}'.format(films_list))
            start = response.meta.get('start')
            genres = response.meta.get('genres')
            year = response.meta.get('year')
            self.logger.info('正在爬取{}{}{}'.format(genres,year,start))
            for film in films_list:
                item = DoubanItem()
                item['movice_url'] = film.get('url')
                item['title'] = film.get('title')
                item['directors'] = film.get('directors')
                item['casts'] = film.get('casts')
                item['rate'] = film.get('rate')
                item['type'] = genres
                yield item

            # if len(films_list) == 20:
            if len(films_list) > 0:
                start += 20
                self.logger.debug('start:{}'.format(start))
                self.logger.debug('正在访问第{}页'.format(start / 20))
                yield scrapy.Request(self.base_urls.format(start,genres,year,year), meta={'start': start,'genres':genres,'year':year})
            else:
                self.logger.info('len(films_list)=0,已经访问到最后一页')
