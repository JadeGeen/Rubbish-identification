from Screening_Strategies.api import api
from multiprocessing import Queue

pic_processed = Queue()


# 算法服务器结果入队
def send_Pic(data):
    pic_processed.put(data)


def stragtegies_work():
    # 单图测试
    count = 0

    while 1:
        if pic_processed.empty():
            continue
        else:
            data = pic_processed.get()
            api(
                data['userID'],
                data['time_msg'],
                data['label'],
                data['bboxs_list'],
                data['pic_array'],
            )
            count += 1

        # for test
        if count >= 1:
            break
