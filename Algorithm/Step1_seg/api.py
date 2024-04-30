import numpy as np
from Step1_seg.utils.clip import clip_pic
from Step1_seg.utils.sam import SamModel, sam_checkpoint, model_type, device

def api(image:np.ndarray , n: int, overlap: float):
    pic_list,bias_list = clip_pic(image, n, overlap)
    model = SamModel(model_type, sam_checkpoint, device)
    masks_list = []
    for pic in pic_list:
        masks_list.append(model.generate_mask(pic))
    bboxs_list = []
    for i in range(len(masks_list)):
        for mask in masks_list[i]:
            tmp = mask['bbox']
            tmp[0] += bias_list[i][0]
            tmp[1] += bias_list[i][1]
            bboxs_list.append(tmp)
    return bboxs_list
    # None