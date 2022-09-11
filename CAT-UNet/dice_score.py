# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 14:01:49 2021

@author: SHIN
"""

import cv2
import os
import numpy as np
from skimage import io, transform

dice = 0.0
fn = 0
fp = 0
for i in range(1,360):
    s2 = cv2.imread('D:/Swin/TransUNet_test/data/label_GT_original(512)/ ' + str(i) + '.bmp', 0)  # 模板
    #s2[s2>=127] = 255
    #s2[s2<127] = 0
    row, col = s2.shape[0], s2.shape[1]
    s1 = cv2.imread("D:/Swin/TransUNet_test/predictions/TU_own512/512(t11_original_CA2)/ " + str(i) + ".png", 0)  # 读取配准后图像
    #print(s1[s1<255])
    #s2[s2>=127] = 255
    #s2[s2<127] = 0

    #print(s1.shape)
    d = []
    s = []
    for r in range(row):
        for c in range(col):
            if s1[r][c] == s2[r][c]:  # 计算图像像素交集
                s.append(s1[r][c])
    m1 = np.linalg.norm(s)
    m2 = np.linalg.norm(s1.flatten()) + np.linalg.norm(s2.flatten())
    #print(s)
    #print(m1)
    #print(m2)

    if(m1>0.0 and m2>0.0):
        d.append(2*m1/m2)
        msg = "第{}張圖的dice係數".format(i) + str(2 * m1 / m2)
        img_dice = (2 * m1 / m2)
        #print(msg)
        dice+=float(img_dice)
    if(m1==0.0 and m2==0.0):
        d.append(1.0)
        msg = "第{}張圖的dice係數".format(i) + str(1.0)
        img_dice = 1.0
        #print(msg)
        dice+=float(img_dice)
    if(m1==0.0 and m2!=0.0):
        msg = "第{}張圖的dice係數".format(i) + str(0.0)
        img_dice = 0.0
        d.append(0.0)
        print(msg)
        dice+=float(img_dice)
        fn+=1
        #print(d)
        
                
print(fn)
print(fp)      
print(dice)
print(dice/359)
