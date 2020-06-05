# -*- coding: utf-8 -*-

from pixivpy3 import *
def gt():
    api = ByPassSniApi()
    api.hosts = 'https://210.140.131.226'
    api.set_auth("","VIDisi2zd9AhcB1VQRuoJB19HXHjT4QrUCcDTocjs0w")
    api.auth()
    return (api.access_token)
#print(api.illust_detail(10001))