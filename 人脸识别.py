
import cv2
import numpy as np
from tensorflow.python.keras.models import load_model

picHeight, picWidth = 100, 100  # 可以在这里直接改图像的高和宽

# ##################################读取人脸#################################
cap = cv2.VideoCapture(0)  # 笔记本内置摄像头
font = cv2.FONT_HERSHEY_SIMPLEX

face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  # haar分类器
print("\n 正在探测人脸，请保持不动")
count = 0

success, img = cap.read()  # 从摄像头读取图片
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转为灰度图片
gray = cv2.equalizeHist(gray)  # 创建平衡直方图，减少光线影响
faces = face_detector.detectMultiScale(gray, 1.2, 3, cv2.CASCADE_SCALE_IMAGE, (40, 60))

for (x, y, w, h) in faces:  # 获取人脸图像
    cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
    count = count + 1
    cv2.putText(img, str(count), (x+5, y-5), font, 1, (0, 0, 255), 1)  # 为图片添加文字
    cv2.imwrite("test_photo.jpg", gray[y:y+h, x: x+w])  # 保存图像
image = cv2.imread("test_photo.jpg")  # 把刚刚读取到的人脸图片imread
re_image = cv2.resize(image, (100, 100))
cv2.imwrite("test_photo.jpg", re_image)  # 修改成对应尺寸后保存

# ################################################识别人脸########################################################
model = load_model('face_recognition.h5')  # 加载模型
photo = cv2.imread("test_photo.jpg")  # 加载图片
resized_photo = cv2.resize(photo, (picHeight, picWidth))  # 调整图片大小
recolord_photo = cv2.cvtColor(resized_photo, cv2.COLOR_BGR2GRAY)  # 调整为灰度图
recolord_photo = recolord_photo.reshape((1, 1, picHeight, picWidth))
recolord_photo = recolord_photo / 255.0
result = model.predict(recolord_photo)  # 人物预测，返回试验集各个类别的概率
max_index = np.argmax(result)  # print(max(result))
name = np.load('name.npy')  # 显示结果
print("是"+name[max_index]+"的概率是"+str(max(result[0])*100)+"%")
print('您好！' + name[max_index]+'先生，今日工作愉快！')






