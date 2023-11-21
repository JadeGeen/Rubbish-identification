from concurrent.futures import ProcessPoolExecutor
from Routes import app_RUN
from Fileprocess import time_cut
from Utils import stragtegies_work


'''
多线程：
1: 轮询摄像头发request
2: 服务器通信
3: 筛选系统工作
'''

# for test
test_ID = 1
test_path = r'Data\Camera.mp4'
test_sec = 60


if __name__ == '__main__':
    e = ProcessPoolExecutor(3)
    e.submit(app_RUN)
    e.submit(time_cut, test_ID, test_path, test_sec)
    e.submit(stragtegies_work)
    e.shutdown()
