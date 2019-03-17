# -*- coding: utf-8 -*-
import scrapy
from nhaccuatui.items import NhaccuatuiItem

class LyricSpider(scrapy.Spider):
    name = 'lyric'
    allowed_domains = ['nhaccuatui.com']
    start_urls = ['http://nhaccuatui.com/bai-hat/nhac-tre-moi.html']

    def parse(self, response):
        linkCategoryList = response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="box_cata_control"]/ul[@class="detail_menu_browsing_dashboard"]/li/a/@href').extract()
        for linkCategory in linkCategoryList:
            yield scrapy.Request(linkCategory, callback=self.crawlCategory)

    def crawlCategory(self, response):
        finalPage = response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="box_pageview"]/a/@href')[-1].extract()
        totalPage = int(finalPage.split(".")[-2])
        for page in range(totalPage):
            link = finalPage.replace(str(totalPage), str(page + 1))
            yield scrapy.Request(link, callback=self.crawlLyric)

    def crawlLyric(self, response):
        for linkLyric in response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="list_music_full"]/div[@class="fram_select"]/div[@class="list_music listGenre"]/div[@class="fram_select"]/ul[@class="listGenre"]/li/div[@class="box-content-music-list"]/div[@class="info_song"]/a[@class="avatar_song"]/@href').extract():
            yield scrapy.Request(linkLyric, callback=self.saveFile)

    def saveFile(self, response):
      lyricRaw = response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="lyric"]/p[@id="divLyric"]/text()').extract()
      lyric = "\n".join(lyricRaw[1:])
      item = NhaccuatuiItem()
      item['name'] = lyricRaw[0].encode("utf-8")
      item['lyric'] = lyric.encode("utf-8")
      item['link'] = response.url.encode("utf-8")
      yield item
