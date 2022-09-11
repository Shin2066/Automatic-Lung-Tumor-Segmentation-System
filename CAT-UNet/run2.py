import cv2
import numpy as np
import os
from PIL import Image
from test2 import test2
from convert_image import dicom_to_image

def overimage():
    yourPath = original_path+r"x_rays\val\images"
    path = original_path+r"CAT-UNet\predict"
    allFileList = os.listdir(yourPath)
    total_image=0
    mass = 0
    normal = 0
    data=open(original_path+r"CAT-UNet\temp\output.txt",'w+') 
    for file in allFileList:
        total_image+=1
        #print(file)
        original = cv2.imread(yourPath+"/"+file)
        #img = Image.open(os.path.join(path,file)).convert('RGB')
        mask = cv2.imread(path+"/"+file)
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
        cv2.imwrite(original_path+r"result/"+file,overimage)
        #紅色GT 白色predict
    data.close()
    # print(total_image)  #影像total
    # print(normal)
    # print(mass)
    data2=open(original_path+r"CAT-UNet\temp\total.txt",'w+') 
    print(total_image,file=data2)
    print(normal,file=data2)
    print(mass,file=data2)
    data2.close()

    
if __name__ == "__main__":
    original_path = "D:/UI/"  ###修改此路徑
    x_rays = (original_path+"x_rays/val/images/")
    x_rays_path = os.listdir(x_rays)
    for file_image in x_rays_path:
        print(file_image)
        os.remove(x_rays+file_image)
    with open(original_path+r"CAT-UNet\temp\path.txt") as f:
        firstline = f.readlines()[0].rstrip()
    dicom_to_image(in_dir=firstline,
                    out_dir=original_path+r"x_rays\val\images", HU=False)
    test2(original_path)
    overimage()