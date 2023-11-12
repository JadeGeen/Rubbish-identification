from match import img_similarity

class my_struct:
    def __init__(self, camera_id, time_msg, label_value, bboxs_list, pic_array):
        self.camera_id = camera_id
        self.time = time_msg
        self.label = label_value
        self.bboxs_list = bboxs_list
        self.pic_array = pic_array


def screening_startegies(pic : my_struct, ctex:list)->int:
# TODO：筛选策略，具体参数和返回值待定
    return pic.label