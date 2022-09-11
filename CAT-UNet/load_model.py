def intersect_dicts(da, db, exclude=()):  #取權重的交集
    # Dictionary intersection of matching keys and shapes, omitting 'exclude' keys, using da values
    return {k: v for k, v in da.items() if k in db and not any(x in k for x in exclude) and v.shape == db[k].shape}


ckpt = torch.load('D:/Shin/TransUNet_test/model/vit_checkpoint/imagenet21k/imagenet21k+imagenet2012_R50+ViT-B_16.pth')  #載入權重
csd = ckpt.state_dict()  #得到函數對應的參數
csd = intersect_dicts(csd, net.state_dict())  # intersect
print(len(csd))
#print(csd.keys())  #輸出key名稱
net.load_state_dict(csd, strict=False)  # load