import os
import cv2 as cv

def save_img(video_path,save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path,exist_ok=True)
    cap = cv.VideoCapture(video_path)
    idx = 0
    while cap.isOpened():
        idx = idx + 1
        ret,frame = cap.read()
        if not ret:
            print("finish video to img")
            break
        cv.imwrite(os.path.join(save_path,"frame_"+str(idx)+".png"),frame)

    cap.release()
    pass


if __name__ == '__main__':
    video_path = '/Users/yanghongchao/Desktop/ml/ChangeDetection/src/test3.mp4'
    save_path = '/Users/yanghongchao/Desktop/ml/ChangeDetection/data/frames'
    save_img(video_path,save_path)