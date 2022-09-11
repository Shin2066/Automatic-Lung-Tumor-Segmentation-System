import os
import cv2
import random
import numpy as np
from shutil import copyfile, move
from PIL import Image
import torch
import torch.utils.data as data
from torchvision import transforms
from datasets import custom_transforms as tr

def read_own_data(root_path, split = 'train'):
    images = []
    masks = []

    image_root = os.path.join(root_path, split + '/images')
    gt_root = os.path.join(root_path, split + '/labels')


    for image_name in os.listdir(image_root):
        image_path = os.path.join(image_root, image_name)
        label_path = os.path.join(gt_root, image_name)

        images.append(image_path)
        masks.append(label_path)

    return images, masks

def own_data_loader(img_path, mask_path):
    img = Image.open(img_path).convert('RGB')
    mask = Image.open(mask_path)
    mask = np.array(mask)
    mask[mask>0] = 1     #这里我把255转到了1
    mask = Image.fromarray(np.uint8(mask))
    return img, mask

class ImageFolder(data.Dataset):

    def __init__(self, args, split='train'):
        self.args = args
        self.root = self.args.root_path
        self.split = split
        self.images, self.labels = read_own_data(self.root, self.split)
    
    def transform_tr(self, sample):
        composed_transforms = transforms.Compose([
            #tr.RandomHorizontalFlip(),
            tr.RandomScaleCrop(base_size=self.args.base_size, crop_size=self.args.img_size),
            #隨機裁剪成一定長寬比再縮放
            tr.RandomGaussianBlur(),
            #高斯模糊
            #tr.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)),
            tr.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            tr.ToTensor()
            ])
        return composed_transforms(sample)

    def transform_val(self, sample):
        composed_transforms = transforms.Compose([
            tr.FixScaleCrop(crop_size=self.args.img_size),
            #tr.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)),
            tr.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            tr.ToTensor()
            ])
        return composed_transforms(sample)

    def __getitem__(self, index):
        img, mask = own_data_loader(self.images[index], self.labels[index])
        if self.split == "train":
            sample = {'image': img, 'label': mask}
            return self.transform_tr(sample)
        elif self.split == 'val':
            img_name = os.path.split(self.images[index])[1]
            sample = {'image': img, 'label': mask}
            sample_ = self.transform_val(sample)
            sample_['case_name'] = img_name[0:-4]
            return sample_
        # return sample

    def __len__(self):
        assert len(self.images) == len(self.labels), 'The number of images must be equal to labels'
        return len(self.images)
