# -*- coding: utf-8 -*-
import numpy
import cv2
import pymongo
import pickle
from bson.binary import Binary

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
maincol = myclient["ImgSearch"]["Main"]

orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING2)
def readImgHash(filename,hash_size = 64):
    with open(filename,"rb") as f:
        return orb.detectAndCompute(cv2.imdecode(numpy.asarray(bytearray(f.read()),dtype='uint8'), 0),None)[1]
def compareHash(h1,h2):
    matches = bf.knnMatch(h2, trainDescriptors = h1, k = 2)
    good = [m for (m,n) in matches if m.distance < 0.75*n.distance]
    return len(good)/500

mhash = readImgHash("74128888.jpg")
collection = maincol.find()

found = [(0.0,"None")]

for col in collection:
    difference = compareHash(mhash,pickle.loads(col["hash"]))
    if found[-1][0] < difference:
        found.append((difference,col["id"]))
        if len(found) > 5:
            found.pop(0)

print(found)