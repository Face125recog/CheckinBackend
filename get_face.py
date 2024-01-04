# -*- coding: utf-8 -*-
import cv2
import os
from os import listdir
import numpy as np
from utility import LastFileNum
from utility import RenameAllFirst
from utility import RenameAllLast

cap = cv2.VideoCapture(0)  # 笔记本内置摄像头
font = cv2.FONT_HERSHEY_SIMPLEX

face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  # haar分类器
face_id = input("\n 请输入您的工号:")  # 训练者的工号（纯数字）
face_name = input("\n 请输入您的名字:")  # 训练者的工号（纯数字）
print("\n 正在初始化面部特征。请注视摄像头，等待一会...")
count = 0

bool_ = os.path.exists("faces/" + str(face_id))  # 判定文件夹是否存在，不存在的话就生成
if bool_:
    pass  # 存在就无事发生
else:
    os.makedirs("faces/" + str(face_id))  # 不存在的话就生成
floder_path = "faces/" + str(face_id)
RenameAllFirst(floder_path)  # 别问为什么要分First跟last，混在一起跑不起来就分开了别问。。。其实也可以合起来但我懒写完懒得改
RenameAllLast(floder_path)
start = LastFileNum(floder_path)
print(start)
while True:
    success, img = cap.read()  # 从摄像头读取图片
    if img is None:
        print("none")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转为灰度图片
    gray = cv2.equalizeHist(gray)  # 创建平衡直方图，减少光线影响
    faces = face_detector.detectMultiScale(gray, 1.2, 3, cv2.CASCADE_SCALE_IMAGE, (40, 60))


    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
        count = count + 1
        cv2.putText(img, str(count), (x+5, y-5), font, 1, (0, 0, 255), 1)  # 为图片添加文字
        print("目前是第"+str(count)+"轮次...")
        cv2.imwrite("faces/"+str(face_id)+"/"+str(count+start)+".jpg", gray[y:y+h, x: x+w])  # 保存图像
        cv2.imshow("image", img)
    k = cv2.waitKey(1)  # 保持画面持续
    if k == 27:  # esc键退出图像
        break
    elif count >= 10:  # 得到对应数量样本后退出摄像
        break

print("正在重置录入数据分辨率...")

FileDir = listdir("faces/"+str(face_id))  # 修改图片分辨率为对应尺寸

for i in range(len(FileDir)):

    path = "faces/"+str(face_id)+"/"+FileDir[i]
    image = cv2.imread(path)
    re_image = cv2.resize(image, (100, 100))
    cv2.imwrite("faces/"+str(face_id)+"/"+str(count+start)+".jpg", re_image)

print("分辨率重置完毕...")
print("人脸数据收集完毕...")


cap.release()
cv2.destroyAllWindows()
