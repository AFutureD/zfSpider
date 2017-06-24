from PIL import Image
import numpy as np
import os


# 特征提取，获取图像二值化数学值  
def getBinaryPix( im ):
    im = Image.open(im)
    img = np.array(im)
    rows, cols = img.shape
    for i in range(rows):
        for j in range(cols):
            if (img[i, j] <= 128):
                img[i, j] = 0
            else:
                img[i, j] = 1

    binpix = np.ravel(img)
    return binpix


def getfiles( dirs ):
    fs = []
    for fr in os.listdir(dirs):
        f = dirs + fr
        if f.rfind(u'.DS_Store') == -1:
            fs.append(f)
    return fs
