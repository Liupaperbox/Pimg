# -*- coding: utf-8 -*-
import pymongo
from . import hasher


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
maincol = myclient["ImgSearch"]["Main"]

with open("10000_p0.jpg",'rb') as f:
    mhash = hasher.readImgOrbHash(f.read())
collection = maincol.find()

found = [(0.0,"None")]

for col in collection:
    difference = hasher.compareImgOrbHash(mhash,hasher.bin2Hash(col["orbhash"]))
    if found[-1][0] < difference:
        found.append((difference,col["pid"]))
        if len(found) > 5:
            found.pop(0)

print(found)

'''
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
maincol = myclient["ImgSearch"]["Main"]

with open("10000_p0.jpg",'rb') as f:
    mhash = hasher.array2Hash( hasher.readImgHash(f.read()))
collection = maincol.find()

found = [(0.0,"None")]

for col in collection:
    difference = hasher.compareImgHash(mhash,hasher.array2Hash(hasher.bin2Hash(col["imghash"])))
    if found[-1][0] < difference:
        found.append((difference,col["pid"]))
        if len(found) > 5:
            found.pop(0)

print(found)
'''