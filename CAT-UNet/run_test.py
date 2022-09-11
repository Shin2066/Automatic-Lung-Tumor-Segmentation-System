import cv2
import numpy as np
import os
from PIL import Image
from test2 import test2
from convert import dicom_to_image

def overimage():
    yourPath = "D:/UI/CAT-UNet/x_rays_data/val/images/"
    path = "D:/UI/CAT-UNet/predict/"
    allFileList = os.listdir(yourPath)
    total_image=0
    mass = 0
    normal = 0
    data=open("D:/UI/CAT-UNet/temp/output.txt",'w+') 
    for file in allFileList:
        total_image+=1
        #print(file)
        original = cv2.imread(yourPath+file)
        img = Image.open(os.path.join(path,file)).convert('RGB')
        mask = cv2.imread("D:/UI/CAT-UNet/predict/"+file)
        #判斷影像是否有Mass 全黑--->Normal/有白色--->mass
        if np.mean(mask) == 0:
            #print("block")
            normal+=1
            print("Normal",file=data)
        else:
            #print("white")
            mass+=1
            print("Mass",file=data)
        #
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
        cv2.imwrite('D:/UI/CAT-UNet/result/'+file,overimage)
        #紅色GT 白色predict
    # print(total_image)  #影像total
    # print(normal)
    # print(mass)
    data2=open("D:/UI/CAT-UNet/temp/total.txt",'w+') 
    print(total_image,file=data2)
    print(normal,file=data2)
    print(mass,file=data2)
    data.close()

    
if __name__ == "__main__":
    with open("D:/UI/CAT-UNet/temp/path.txt") as f:
        firstline = f.readlines()[0].rstrip()
    dicom_to_image(in_dir=firstline,
                    out_dir=r"D:\UI\CAT-UNet\x_rays_data\val\images", HU=False)
    test2()
    overimage()