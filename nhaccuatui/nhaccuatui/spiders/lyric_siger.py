# -*- coding: utf-8 -*-
import scrapy
from nhaccuatui.items import NhaccuatuiItem


class LyricSingerSpider(scrapy.Spider):
    name = 'lyric_singer'
    allowed_domains = ['nhaccuatui.com']
    start_urls = ['http://nhaccuatui.com/nghe-si.html']

    def parse(self, response):
        linkCategorySingerList = response.xpath(
            '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-singer-full"]/div[@class="tile_box_key"]/div[@class="sing-select-abc"]/a/@href').extract()
        linkCategorySingerList.pop(0)
        for linkCategorySinger in linkCategorySingerList:
            yield scrapy.Request(linkCategorySinger, callback=self.crawlCategorySinger)

    def crawlCategorySinger(self, response):
        try:
            finalPage = response.xpath(
                '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-singer-full"]/div[@class="box_pageview"]/a/@href')[-1].extract()
            totalPage = int(finalPage.split(".")[-2])
            for page in range(totalPage):
                link = finalPage.replace(str(totalPage), str(page + 1))
                yield scrapy.Request(link, callback=self.crawlSinger)
        except:
            link = response.xpath(
                '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-singer-full"]/div[@class="tile_box_key"]/div[@class="sing-select-abc"]/a[@class="active"]/@href').extract()
            yield scrapy.Request(link[0], callback=self.crawlSinger)

    def crawlSinger(self, response):
        linkSingerList1 = response.xpath(
            '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-singer-full"]/ul[@class="list-singer-item"]/li/a/@href').extract()
        linkSingerList2 = response.xpath(
            '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-singer-full"]/ul[@class="list-singer-item-more"]/li/h3/a/@href').extract()
        linkSingerList = linkSingerList1 + linkSingerList2
        for linkSinger in linkSingerList:
            linkSongOfSinger = ''.join([linkSinger[:-4], 'bai-hat.html'])
            yield scrapy.Request(linkSongOfSinger, callback=self.crawlSongOfSinger)

    def crawlSongOfSinger(self, response):
        try:
            finalPage = response.xpath(
                '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="box_pageview"]/a/@href')[-1].extract()
            totalPage = int(finalPage.split(".")[-2])
            for page in range(totalPage):
                link = finalPage.replace(str(totalPage), str(page + 1))
                yield scrapy.Request(link, callback=self.crawlLyric)
        except:
            link = response.url
            yield scrapy.Request(link, callback=self.crawlLyric)

    def crawlLyric(self, response):
        linkLyricList = response.xpath(
            '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="list_music_full"]/div[@class="list_music listGenre"]/div[@class="fram_select"]/ul[@class="listGenre"]/li/div[@class="box-content-music-list"]/div[@class="info_song"]/a[@class="avatar_song"]/@href').extract()
        for linkLyric in linkLyricList:
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
