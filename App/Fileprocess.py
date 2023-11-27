import cv2
import requests
from datetime import datetime

from Config import config

test_save_path = r'Data'

# 切帧
def fileprocess(url):
    video = cv2.VideoCapture(url)
    ret, pic = video.read()
    cut_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cv2.imencode('.jpg', pic)[1].tofile(test_save_path + "\\test.jpg")
    video.release()
    return pic, cut_time


def time_cut(ID, url, time):
    # 单视频单图测试
    pic, cut_time = fileprocess(url)
    requests.post(
        config['Alg_addr']+'/upload', data={'pic': pic, 'time_msg': cut_time, 'userID': ID}
    )

    '''
    video = cv2.VideoCapture(url)
    while True:
        ret, frame = video.read()
        FPS = video.get(5)
        if ret:
            frameRate = int(FPS) * time
            if c % frameRate == 0:
                print("cut:" + str(c))
                cv2.imwrite("./capture_image/" + str(c) + '.jpg', frame)
            c += 1
            cv2.waitKey(0)
        else:
            print("所有帧都已经保存完成")
            break    
    '''
