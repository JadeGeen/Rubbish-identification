from database import table_check, data_save, data_load
from Strategies import screening_startegies, my_struct
import numpy as np


def api(camera_id:int, time_msg:str, label, bboxs_list : list, pic:np.ndarray)->None:
    data = my_struct(camera_id=camera_id, time_msg=time_msg, label_value=label, bboxs_list= bboxs_list, pic_array=pic)
    table_check()
    # 获取相关摄像头上下文(暂未定时间范围，全取)
    ctext = data_load(data.camera_id)
    # 筛选获取新label
    new_label = screening_startegies(data, ctext)
    data.label = new_label
    # 存储筛选后的数据
    data_save(data)

# 用于用户查询数据库
def api_search(camera_id:int, time_msg:str)->my_struct:
    """
    :param camera_id: 摄像头编号
    :param time: 时间信息
    :return: 是否清理干净
    """
    result = data_load(camera_id=camera_id, time=time_msg)
    return result.label