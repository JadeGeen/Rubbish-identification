import threading
from Routes import app_RUN
from Fileprocess import time_cut, local_single_test


'''
多线程：
1: 轮询摄像头发request(仅单视频测试，后续删除，由服务器自动生成线程)
2: 服务器通信
'''

# for test
test_ID = 50000
test_URL = "Data/Camera.mp4"


if __name__ == '__main__':
    t1 = threading.Thread(
        target=local_single_test,
        args=(test_ID, test_URL),
    )
    t2 = threading.Thread(target=app_RUN)
    t1.start()
    t2.start()
