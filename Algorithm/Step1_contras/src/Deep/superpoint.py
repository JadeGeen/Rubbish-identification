import numpy as np
import time

from ChangeDetection.SuperPointPretrainedNetwork import superpoint as sp
import cv2
from ChangeDetection.src.Deep.base import main
from ChangeDetection.src.traditional import sift
from ChangeDetection.src.traditional import new_muliti_homography

superpoint = sp.init_super_point()
kp1 = None
desc1 = None

def get_kp_and_des_sp(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img.astype('float32') / 255.0
    kp, des,_ =  superpoint.run(img)
    return np.transpose(kp),np.transpose(des)

def get_kp_and_des_sp_keypoint(img):
    pts,des = get_kp_and_des_sp(img)
    kps = [cv2.KeyPoint(pts[i][0], pts[i][1],pts[i][2])
              for i in range(pts.shape[0])]
    return kps,des

def get_des_from_kp_sp(img,kp):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img.astype('float32') / 255.0
    des = superpoint.get_des(img,kp)
    return np.transpose(des)

def match_img(des1,des2,threshold=0.7):
    return sp.nn_match_two_way(des1,des2,threshold)
def sp_detect(img1,img2,th1=0.85,th2=0.25,threshold = 550):
    # return main(img1,img2,get_kp_and_des_sift,get_des_from_kp_sift,threshold)
    global kp1,desc1
    if kp1 is None:
        img1 = cv2.GaussianBlur(img1, (5, 5), 0)
        kp1,desc1 = get_kp_and_des_sp_keypoint(img1)
        print("kp1 finished!")
    img2 = cv2.GaussianBlur(img2, (5, 5), 0)
    kp2,desc2 = get_kp_and_des_sp_keypoint(img2)
    return new_muliti_homography.main(img1,img2,kp1,desc1,kp2,desc2,sift.get_des_from_kp_sift,threshold,th1,th2)


def sp_detect_two(img1,img2,th1=0.85,th2=0.25,threshold = 550):
    # return main(img1,img2,get_kp_and_des_sift,get_des_from_kp_sift,threshold)
    img1 = cv2.GaussianBlur(img1, (5, 5), 0)
    kp1,desc1 = get_kp_and_des_sp_keypoint(img1)
    img2 = cv2.GaussianBlur(img2, (5, 5), 0)
    kp2,desc2 = get_kp_and_des_sp_keypoint(img2)
    return new_muliti_homography.main(img1,img2,kp1,desc1,kp2,desc2,sift.get_des_from_kp_sift,threshold,th1,th2)