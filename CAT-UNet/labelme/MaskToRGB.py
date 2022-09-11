# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 17:35:05 2021

@author: SHIN
"""

import os
import cv2
from PIL import Image
from pathlib import Path
path='C:/Users/iris-yuntech/anaconda3/envs/labelme/Lib/site-packages/labelme/cli/0418_newcut/mask_block'
total = os.listdir(path)
#num=len(total)

for file in total:
    #filename=str(i)+'_mask.png'
    #filename='mass_'+str(i)+'_mask.png'
        print(file)
        img=os.path.join(path,file)
        #img = cv2.imread(path+'/'+file)
        mask=Image.open(img).convert('L')
        mask.putpalette([0, 0, 0,  # putpalette给对象加上调色板，相当于上色：背景为黑色，目标１为红色，目标2为黄色，目标3为橙色（如果你的图中有更多的目标，可以自行添加更多的调色值）
                         255, 255, 255,
                         0, 0, 0,
                         0, 0, 0])
        
        savepath = 'C:/Users/iris-yuntech/anaconda3/envs/labelme/Lib/site-packages/labelme/cli/0418_newcut/mask_bmp'
        #filename2=str(i)+'.png'
        file = file_name = Path(file).stem
        filename2=file+'.bmp'
        mask.save(os.path.join(savepath,filename2))

"""
mask.putpalette([0, 0, 0,  # putpalette给对象加上调色板，相当于上色：背景为黑色，目标１为红色，目标2为黄色，目标3为橙色（如果你的图中有更多的目标，可以自行添加更多的调色值）
                 255, 0, 0,
                 255, 255, 0,
                 255, 153, 0])
"""