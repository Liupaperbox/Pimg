import cv2
import numpy
import pickle
from PIL import Image
import imagehash
from io import BytesIO
from bson.binary import Binary

orb = cv2.ORB_create()
def readImgHash(byte,hash_size=16):
    return imagehash.average_hash(Image.open(BytesIO(byte)),hash_size=hash_size).hash
def readImgOrbHash(byte,hash_size = 64):
    return orb.detectAndCompute(cv2.imdecode(numpy.asarray(bytearray(byte),dtype='uint8'), 0),None)[1]
def hash2Bin(mhash):
    return Binary(pickle.dumps(mhash, protocol=-1), subtype=128)
def bin2Hash(bina):
    return pickle.loads(bina)
def array2Hash(arr):
    return imagehash.ImageHash(arr)
bf = cv2.BFMatcher(cv2.NORM_HAMMING2)
def compareImgHash(h1,h2):
    return 1 - (h1 - h2)/len(h1.hash)**2
def compareImgOrbHash(h1,h2):
    matches = bf.knnMatch(h2, trainDescriptors = h1, k = 2)
    good = [m for (m,n) in matches if m.distance < 0.75*n.distance]
    return len(good)/500