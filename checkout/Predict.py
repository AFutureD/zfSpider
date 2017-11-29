from sklearn.externals import joblib
import os

from checkout.split_pic import *
from checkout.write_img import *
from PIL import Image


def cutPictures2( name ):
    im = imgTransfer(name)
    pics = segment(im)
    ky = 0
    for pic in pics:
        dir = os.getcwd() + '/checkout/test_picture/%s.jpeg' % ky
        pic.save(dir , 'jpeg')
        ky = ky + 1


def load_Predict( name ):

    cutPictures2(name)  # 切割图片

    dirs = os.getcwd() + '/checkout/test_picture/'
    fs = []  # 获取图片名称
    for i in range(4):
        fn = str(i) + '.jpeg'
        fs.append(fn)
    clf = joblib.load(os.getcwd() + '/checkout/' +  "train_model.m")
    predictValue = []

    for fname in fs:
        fn = dirs + fname
        binpix = getBinaryPix(fn)
        predictValue.append(clf.predict(binpix))

    predictValue = [str(int(i)) for i in predictValue]
    fname = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
             'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    for i in range(4):
        predictValue[i] = fname[int(predictValue[i])]

    ans = ''.join(predictValue)
    for fname in fs:
        fn = dirs + fname
        if os.path.exists(fn):
            os.remove(fn)

    return ans


# im = Image.open(DstDir)
# im = im.convert('RGB')
# im.save(DstDir, 'jpeg')
# print(DstDir)
# code = Predict.load_Predict(DstDir)