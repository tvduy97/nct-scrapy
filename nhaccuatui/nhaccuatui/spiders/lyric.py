# -*- coding: utf-8 -*-
import scrapy
from nhaccuatui.items import NhaccuatuiItem


class LyricSpider(scrapy.Spider):
    name = 'lyric'
    allowed_domains = ['nhaccuatui.com']
    start_urls = ['http://nhaccuatui.com/bai-hat/nhac-tre-moi.html']

    def parse(self, response):
        linkCategoryList = response.xpath(
            '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="box_cata_control"]/ul[@class="detail_menu_browsing_dashboard"]/li/a/@href').extract()
        for linkCategory in linkCategoryList:
            yield scrapy.Request(linkCategory, callback=self.crawlCategory)

    def crawlCategory(self, response):
        finalPage = response.xpath(
            '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="box_pageview"]/a/@href')[-1].extract()
        totalPage = int(finalPage.split(".")[-2])
        for page in range(totalPage):
            link = finalPage.replace(str(totalPage), str(page + 1))
            yield scrapy.Request(link, callback=self.crawlLyric)

    def crawlLyric(self, response):
        for linkLyric in response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="list_music_full"]/div[@class="fram_select"]/div[@class="list_music listGenre"]/div[@class="fram_select"]/ul[@class="listGenre"]/li/div[@class="box-content-music-list"]/div[@class="info_song"]/a[@class="avatar_song"]/@href').extract():
            yield scrapy.Request(linkLyric, callback=self.saveFile)

    def saveFile(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_singer(query):
            return response.css(query).getall()

        def extract_lyric(query):
            sentences = response.css(query).getall()
            lyric = ''
            for st in sentences:
                lyric = lyric + st.strip()
                lyric = lyric + " "
            if u"- Hiện chưa có lời bài hát nào" in lyric:
                return ''
            else:
                return lyric

        item = NhaccuatuiItem()
        item['title'] = extract_with_css('div.name_title h1::text')
        item['singer'] = extract_singer(
            'div.name_title h2 a.name_singer::text')
        item['lyric'] = extract_lyric('#divLyric *::text')
        item['id'] = response.url
        yield item
