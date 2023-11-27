import numpy as np
import cv2 as cv
import torch

from Step1_contras.api import api as Step1_contras_api
from Step1_seg.api import api as Step1_seg_api
from Step2_cls.api import api as Step2_cls_api

def api(target : np.ndarray, contra : bool, base : np.ndarray = np.array([0])):
    seg = 10
    overlap = 1.0
    if contra:
        target, box_list = Step1_contras_api(base, target)
    else:
        box_list = Step1_seg_api(target, seg, overlap)
    res = {}
    for box in box_list:
        img = target[box[0] : box[1], box[2] : box[3]] #切割图片
        image = torch.from_numpy(img)
        info = Step2_cls_api(image)
        res[img] = info
    return res