import argparse
import json
import os
import os.path as osp
import warnings
import copy
import numpy as np
import PIL.Image
import cv2
#from skimage import io
import yaml
from labelme import utils
from PIL import Image
from pathlib import Path
from shutil import copy


def json_to_png():

    list = os.listdir('D:/UI/CAT-UNet/NG/')   # 获取json文件列表
    for i in range(0, len(list)):
        path = os.path.join('D:/UI/CAT-UNet/NG/', list[i])  # 获取每个json文件的绝对路径
        filename = list[i][:-5]       # 提取出.json前的字符作为文件名，以便后续保存Label图片的时候使用
        extension = list[i][-4:]
        if extension == 'json':
            if os.path.isfile(path):
                data = json.load(open(path))
                img = utils.image.img_b64_to_arr(data['imageData'])  # 根据'imageData'字段的字符可以得到原图像
                # lbl为label图片（标注的地方用类别名对应的数字来标，其他为0）lbl_names为label名和数字的对应关系字典
                lbl, lbl_names = utils.shape.labelme_shapes_to_label(img.shape, data['shapes'])   # data['shapes']是json文件中记录着标注的位置及label等信息的字段
                PIL.Image.fromarray(lbl).convert('L').save(osp.join('D:/UI/CAT-UNet/relabel', '{}.png'.format(filename)))
                
#####
def png_toRGBmask():
    path2='D:/UI/CAT-UNet/relabel/'
    train_imagepath='D:/UI/CAT-UNet/x_rays_data/train/images/'
    train_maskpath='D:/UI/CAT-UNet/x_rays_data/train/labels/'
    total = os.listdir(path2)
    #num=len(total)
    
    for file in total:
            img=os.path.join(path2,file)
            #img = cv2.imread(path2+file)
            #mask=Image.open(img).convert('L')
            mask=Image.open(img)
            mask.putpalette([0, 0, 0,  # putpalette给对象加上调色板，相当于上色：背景为黑色，目标１为红色，目标2为黄色，目标3为橙色（如果你的图中有更多的目标，可以自行添加更多的调色值）
                             255, 255, 255,
                             0, 0, 0,
                             0, 0, 0])
            

            file = Path(file).stem
            #print(file)
            filename2=file+'.bmp'
            mask.save(os.path.join(path2,filename2))
            os.remove(path2+file+'.png')
            copy(path2+filename2,train_maskpath+filename2)
def overimage():
    yourPath = 'D:/UI/CAT-UNet/NG/'
    path = "D:/UI/CAT-UNet/relabel/"
    train_imagepath='D:/UI/CAT-UNet/x_rays_data/train/images/'
    allFileList = os.listdir(path)
    for file in allFileList:
        #print(file)
        original = cv2.imread(yourPath+file)
        print(yourPath+file)
        Image.open(os.path.join(path,file)).convert('RGB')
        mask = cv2.imread(path+file)
        print(path+file)
        b_channel, g_channel, r_channel = cv2.split(mask)
        #  使用cv2.threshold函数，输入BRG三个通道的灰度图像，和触发阈值，和转换值，还有触发器类型
        ret1,b = cv2.threshold(b_channel,1,0,cv2.THRESH_BINARY)
        ret2,g = cv2.threshold(g_channel,1,0,cv2.THRESH_BINARY)
        ret3,r = cv2.threshold(r_channel,1,255,cv2.THRESH_BINARY)
        
        dst = cv2.merge((b,g,r))
        
        #255 255 255
        #255 0 0
    
        
        
        # 融合
        overimage =cv2.addWeighted(original,1,dst,0.5,0)
        
        #cv2.imwrite('D:/Shin/TransUNet_test/data/overimage/512_lung_label/'+'mass_'+str(i) + '_0_0.bmp',overimage)
        cv2.imwrite(path+file,overimage)
        copy(yourPath+file,train_imagepath+file)
        #紅色GT 白色predict
    
if __name__ == '__main__':
    json_to_png()
    png_toRGBmask()
    overimage()

