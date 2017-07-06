from PIL import Image, ImageEnhance, ImageFilter
from PIL import *
import time
import os


# 利用crop将图片裁成四块
def segment( im ):
    s = 4
    w = 12
    h = 25
    t = 0
    im_new = []

    for i in range(4):
        im1 = im.crop((s + w * i, t, s + w * (i + 1), h))
        # im.crop剪裁图片
        im_new.append(im1)
    return im_new


# 图片预处理，二进制化，图片增强
def imgTransfer( f_name ):
    im = Image.open(f_name)
    im = im.filter(ImageFilter.MedianFilter())
    # 滤镜medianfilter是中值滤波器作用是减少噪声
    im = im.convert('L')
    # convert图像模式转换转为Ｌ模式 笔记：PIL库共有９种模式

    return im
