# -*- coding: utf-8 -*-
import os
import cv2
import pymongo
import numpy
import pickle
from bson.binary import Binary

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
maincol = myclient["ImgSearch"]["Main"]

maincol.delete_many({})


orb = cv2.ORB_create()
def readImgHash(filename,hash_size = 64):
    with open(filename,"rb") as f:
        return orb.detectAndCompute(cv2.imdecode(numpy.asarray(bytearray(f.read()),dtype='uint8'), 0),None)[1]

path = "E:\\Pictures"
for i in os.listdir(path):
    if i.find("_p") > 0 and(i.find(".jpg") > 0 or i.find(".png") > 0):
        filepath = os.path.join(path,i)
        fileid = i[:i.find(".")]
        mhash = readImgHash(filepath)
        filedict = {"id":fileid,"hash":Binary(pickle.dumps(mhash, protocol=-1), subtype=128)}
        x = maincol.insert_one(filedict) 
        print(x)