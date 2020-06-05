# -*- coding: utf-8 -*-
import scrapy
from imgspider.items import ImgItem
from . import hasher
import json
from pixivpy3 import *
def gt():
    api = ByPassSniApi()
    api.hosts = 'https://210.140.131.226'
    api.set_auth("","VIDisi2zd9AhcB1VQRuoJB19HXHjT4QrUCcDTocjs0w")
    api.auth()
    return api.access_token
#scrapy crawl pixiv

class PixivSpider(scrapy.Spider):
    name = 'pixiv'
    allowed_domains = ['pixiv.net','pximg.net']
    host = 'https://210.140.131.226'
    access_token = 'mUbGxobKEgIO-ldroh-1lASSVSBBcaioWQx17qbczIU'
    def start_requests(self):
        start = 80001968
        headers = {'App-OS':'ios',
                   'App-OS-Version':'12.2',
                   'App-Version':'7.6.2',
                   'host': 'app-api.pixiv.net',
                   'User-Agent':'PixivIOSApp/7.6.2 (iOS 12.2; iPhone9,1)',
                   'Authorization':'Bearer %s' % self.access_token}
        for pid in range(start,start + 100000):
            url = "%s/v1/illust/detail?illust_id=%s"%(self.host,pid)
            yield scrapy.Request(url=url,headers = headers,
            callback=self.dealImg)

    def dealImg(self,response):
        if response.status == 400:
            self.access_token = gt()
            headers = {'App-OS':'ios',
                   'App-OS-Version':'12.2',
                   'App-Version':'7.6.2',
                   'host': 'app-api.pixiv.net',
                   'User-Agent':'PixivIOSApp/7.6.2 (iOS 12.2; iPhone9,1)',
                   'Authorization':'Bearer %s' % self.access_token}
            return scrapy.Request(url=response.url,headers = headers,
            callback=self.dealImg)
        jsonres = json.loads(response.text)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': 'https://www.pixiv.net/'
        }
        if "error" in jsonres:
            return 
        pid = jsonres["illust"]["id"]
        url = jsonres["illust"]["image_urls"]["large"]
        print(jsonres)
        yield scrapy.Request(url=url, meta={'pid': pid},headers = headers,
            callback=self.parse)
        

    def parse(self, response):
        pid = response.meta['pid']
        item = ImgItem()
        mhash = hasher.readImgOrbHash(response.body)
        ihash = hasher.readImgHash(response.body)
        item["pid"] = pid
        item["platform"] = 0
        item["orbhash"] = hasher.hash2Bin(mhash)
        item["imghash"] = hasher.hash2Bin(ihash)
        return item
        
        
