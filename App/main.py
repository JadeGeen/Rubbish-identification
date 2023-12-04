import threading
from Routes import app_RUN
from Fileprocess import time_cut


'''
多线程：
1: 轮询摄像头发request
2: 服务器通信
'''

# for test
test_ID = 1
test_path = r'Data/Camera.mp4'
test_sec = 60


if __name__ == '__main__':
    t1 = threading.Thread(
        target=time_cut,
        args=(
            test_ID,
            test_path,
            test_sec,
        ),
    )
    t2 = threading.Thread(target=app_RUN)
    t1.start()
    t2.start()
