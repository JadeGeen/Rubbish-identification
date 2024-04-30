# -*- coding: utf-8 -*-
import cv2
import numpy as np
from Step1_contras.src.traditional.base import main
from Step1_contras.src.traditional import base_muliti_homography

#sift = cv2.xfeatures2d.SIFT_create()
sift = cv2.SIFT_create()

def get_kp_and_des_sift(img):
    return sift.detectAndCompute(img, None)

def get_des_from_kp_sift(img,kp):
    _, descriptors_image = sift.compute(img, kp)
    return np.asarray(descriptors_image, np.float32)

def sift_detect(img1,img2,threshold = 550):
    # return main(img1,img2,get_kp_and_des_sift,get_des_from_kp_sift,threshold)
    return base_muliti_homography.main(img1,img2,get_kp_and_des_sift,get_des_from_kp_sift,threshold)