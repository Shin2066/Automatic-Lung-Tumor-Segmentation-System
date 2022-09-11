import argparse
import logging
import os
import random
import numpy as np
import torch
import torch.backends.cudnn as cudnn
from networks.vit_seg_modeling import VisionTransformer as ViT_seg
from networks.vit_seg_modeling import CONFIGS as CONFIGS_ViT_seg
from trainer import trainer_synapse

import torch
torch.cuda.empty_cache()

parser = argparse.ArgumentParser()
parser.add_argument('--root_path', type=str,
                    default='../data/Synapse/train_npz', help='root dir for data')
parser.add_argument('--dataset', type=str,
                    default='own', help='experiment_name')
parser.add_argument('--list_dir', type=str,
                    default='./lists/lists_Synapse', help='list dir')
parser.add_argument('--num_classes', type=int,
                    default=2, help='output channel of network')
parser.add_argument('--max_iterations', type=int,
                    default=30000, help='maximum epoch number to train')
parser.add_argument('--max_epochs', type=int,
                    default=150, help='maximum epoch number to train')
parser.add_argument('--batch_size', type=int,
                    default=4, help='batch_size per gpu')
parser.add_argument('--n_gpu', type=int, default=1, help='total gpu')
parser.add_argument('--deterministic', type=int,  default=1,
                    help='whether use deterministic training')
parser.add_argument('--base_lr', type=float,  default=0.01,
                    help='segmentation network learning rate')
parser.add_argument('--base_size', type=int,
                    default=512, help='input patch size of original input')
parser.add_argument('--img_size', type=int,
                    default=512, help='input patch size of network input')
parser.add_argument('--seed', type=int,
                    default=1234, help='random seed')    #这里修改为0
parser.add_argument('--n_skip', type=int,
                    default=4, help='using number of skip-connect, default is num')
parser.add_argument('--vit_name', type=str,
                    default='R50-ViT-B_16', help='select one vit model')
parser.add_argument('--vit_patches_size', type=int,
                    default=16, help='vit_patches_size, default is 16')
args = parser.parse_args()

def intersect_dicts(da, db, exclude=()):  #取權重的交集
    # Dictionary intersection of matching keys and shapes, omitting 'exclude' keys, using da values
    return {k: v for k, v in da.items() if k in db and not any(x in k for x in exclude) and v.shape == db[k].shape}

if __name__ == "__main__":
    if not args.deterministic:
        cudnn.benchmark = True
        cudnn.deterministic = False
    else:
        cudnn.benchmark = False
        cudnn.deterministic = True

    args.dataset = 'own'
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)
    dataset_name = args.dataset
    dataset_config = {
        'Synapse': {
            'root_path': './data/Synapse/train_npz',
            'list_dir': './lists/lists_Synapse',
            'num_classes': 9,
        },
        'own': {
            'root_path': 'D:/x-ray-data/0109_datasets_old/cut',
            'list_dir': '',
            'num_classes': 2,
        },
    }
    args.num_classes = dataset_config[dataset_name]['num_classes']
    args.root_path = dataset_config[dataset_name]['root_path']
    args.list_dir = dataset_config[dataset_name]['list_dir']
    args.is_pretrain = True

    snapshot_path = "D:/Shin/TransUNet_test/model/4layers/cut_ASPP&CBAM&CA2/"
    #print(snapshot_path)
    if not os.path.exists(snapshot_path):
        os.makedirs(snapshot_path)
    config_vit = CONFIGS_ViT_seg[args.vit_name]
    config_vit.n_classes = args.num_classes
    config_vit.n_skip = args.n_skip
    if args.vit_name.find('R50') != -1:
        config_vit.patches.grid = (int(args.img_size / args.vit_patches_size), int(args.img_size / args.vit_patches_size))
    net = ViT_seg(config_vit, img_size=args.img_size, num_classes=config_vit.n_classes).cuda()
    # print(net)

    #net.load_from(weights=np.load('D:/Shin/TransUNet_test/model/vit_checkpoint/imagenet21k/imagenet21k+imagenet2012_R50+ViT-B_16.npz'))
    #torch.save(net,"D:/Shin/TransUNet_test/model/vit_checkpoint/imagenet21k/imagenet21k+imagenet2012_R50+ViT-B_16.pth")
    #####
    ckpt = torch.load('D:/Shin/TransUNet_test/model/vit_checkpoint/imagenet21k/imagenet21k+imagenet2012_R50+ViT-B_16.pth')  #載入權重
    csd = ckpt.state_dict()  #得到函數對應的參數
    csd = intersect_dicts(csd, net.state_dict())  # intersect
    print(len(csd))
    #print(csd.keys())  #輸出key名稱
    net.load_state_dict(csd, strict=False)  # load
    #####

    # pretext_model = torch.load('D:/Shin/TransUNet_test/model/vit_checkpoint/imagenet21k/test.pth').state_dict()
    # model_dict = net.state_dict()
    # print('new model',len(model_dict))
    # print('old model',len(pretext_model))        
    # #load part weight
    # state_dict = {k:v for k,v in pretext_model.items() if k in model_dict.keys()} #load same name layer weiget
    # dict_name = list(state_dict)
    # print('same pam',len(dict_name))
    # model_dict.update(state_dict)
    # net.load_state_dict(model_dict) 
    # print("------------------------------------------")

    trainer = {'Synapse': trainer_synapse,'own': trainer_synapse,}
    trainer[dataset_name](args, net, snapshot_path)
    