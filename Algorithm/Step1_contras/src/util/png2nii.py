import os.path

from PIL import Image
import numpy as np
import SimpleITK as stik

empt_mat = []

def read_img(img_path):
    img = Image.open(img_path)
    # 这里取png图片的前三个通道，去除第四个透明通道
    img = np.array(img)[:,:,0:3]
    return img


def png2nii(png_path,nii_path):
    img = read_img(img_path=png_path)
    empt_mat.append(img)
    emp = np.array(empt_mat)
    nill_file = stik.GetImageFromArray(emp)
    stik.WriteImage(nill_file,nii_path)

if __name__ == '__main__':
    base_path = '/Users/yanghongchao/Desktop/ml/ChangeDetection/data'
    png_path = os.path.join(base_path,'change_7.png')
    nii_path = os.path.join(base_path,'nii/change_7.nii')
    png2nii(png_path,nii_path)
    print("finish!")