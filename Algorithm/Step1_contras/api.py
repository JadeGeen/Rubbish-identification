import cv2 as cv
import numpy as np
from Step1_contras.src.Deep import superpoint
from typing import Tuple,List


#def api(image1:np.ndarray, image2:np.ndarray, th1:float = 0.85, th2:float = 0.25, th3:int = 550) -> Tuple[np.ndarray,List]:
def api(image1:np.ndarray, image2:np.ndarray, th1:float = 0.85, th2:float = 0.25, th3:int = 550):

    base = cv.resize(image1,(400,600))
    target = cv.resize(image2,(400,600))
    box_list = superpoint.sp_detect_two(base,target,th1,th2,th3)
    #target = np.transpose(target,(2,0,1))
    return target,box_list