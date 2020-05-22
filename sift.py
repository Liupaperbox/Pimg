# -*- coding: utf-8 -*-

imgname1 = '74128888_p0.jpg'
imgname2 = '74128888.jpg'

import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread(imgname1,0)
img2 = cv2.imread(imgname2,0)

orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img2,None)
kp2, des2 = orb.detectAndCompute(img1,None)

print(des2)
bf = cv2.BFMatcher(cv2.NORM_HAMMING2)
matches = bf.knnMatch(des1, trainDescriptors = des2, k = 2)
good = [m for (m,n) in matches if m.distance < 0.75*n.distance]
print(len(good))