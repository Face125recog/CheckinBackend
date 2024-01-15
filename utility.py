import os
import re
import sys
import base64
from PIL import Image
import threading
from io import BytesIO
from databaseOp import DbOperate
import cv2
import numpy as np
import shutil
from tensorflow import keras

from tensorflow.python.keras.models import load_model
from train_model import train_the_model

#考虑到复写需求，照片片不够可以录两次，以及二次识别删除时可以用到这些。
def RenameAllFirst(floder):   #统一修改为其他名字 比如tem1.jpg
    fileList1 = os.listdir(floder)  #文件名字
    print("修改前：" + str(fileList1))
    currentpath = os.getcwd()
    os.chdir(floder)
    num = 1
    for fileName in fileList1:
        pat = ".+\.(jpg|png|gif|py|txt)"
        pattern = re.findall(pat, fileName)
        os.rename(fileName, "te"+(str(num)+'.'+pattern[0]))
        num = num + 1
    print("---------------------------------------------------------")
    os.chdir(currentpath)
    sys.stdin.flush()

def RenameAllLast(floder):    #将tem1.jpg改写为1.jpg,可以实现重命名
    fileList1 = os.listdir(floder)  # 文件名字
    print("修改前：" + str(fileList1))
    currentpath = os.getcwd()
    os.chdir(floder)
    num = 1
    for fileName in fileList1:
        pat = ".+\.(jpg|png|gif|py|txt)"
        pattern = re.findall(pat, fileName)
        os.rename(fileName, (str(num) + '.' + pattern[0]))
        num = num + 1
    print("---------------------------------------------------------")
    os.chdir(currentpath)
    sys.stdin.flush()

def LastFileNum(floderPath):   #返回文件夹内图片数量，下次存入时从该数量开始。
    if os.path.exists(floderPath):
        file_count = len(os.listdir(floderPath))
        return file_count
    else:
        return 0

#面部照片处理的类，用来将b64转换为图片，考虑是否把path改一下
class FaceProcess():
    def __init__(self, face):
        self.path = "temp.jpg"
        self.face = face


    #把base64编码转换我图片并保存到self.path路径上。
    def FaceTrans(self):
        head, context = self.face.split(",")
        image_data = base64.b64decode(context)
        img = Image.open(BytesIO(image_data))
        img = img.convert("L")
        # img = cv2.resize(img, (100, 100))
        img.save(self.path)
        return image_data

    def user_identity(self):
        model = load_model('face_recognition.h5')  # 加载模型
        #model = keras.models.load_model('face_recognition.h5')
        photo = cv2.imread(self.path)
        resized_photo = cv2.resize(photo, (100, 100))  # 调整图片大小
        recolord_photo = cv2.cvtColor(resized_photo, cv2.COLOR_BGR2GRAY)  # 调整为灰度图
        recolord_photo = recolord_photo.reshape((1, 1, 100, 100))
        recolord_photo = recolord_photo / 255.0
        result = model.predict(recolord_photo)  # 人物预测，返回试验集各个类别的概率
        print("result：", result)
        max_index = np.argmax(result)+1
        print("max",max_index)
        confidence = result[0][max_index]

        print("confidence:", confidence)
        db = DbOperate()
        result = db.user_identity(max_index)
        print(result)
        db.close_connection()
        del db
        return result, confidence

    def path_tran(self, new_path):
        self.path = new_path


#存储功能的类
class FacesStorge():
    def __init__(self, id, name, faces:list):
        self.path = "faces/" + str(id-1)  #减去1，文件夹从0开始   数据库从1开始
        self.faces = faces
        self.id = id
        self.name = name
        self.db = DbOperate()

   # def faces_transform(self):
    def add_user(self):
        flag = self.db.add_employee(self.id, self.name)
        if flag:
            return 1


    def write_images(self):
        if os.path.exists(self.path):
            RenameAllFirst(self.path)
            RenameAllLast(self.path)
            start = LastFileNum(self.path)
        else:
            os.makedirs(self.path)
            start = 1

        for face in self.faces:
            face_trans = FaceProcess(face)
            new_path = self.path + '/' +str(start) + '.jpg'
            start = start + 1
            face_trans.path_tran(new_path)
            #print(new_path)
            face_trans.FaceTrans()


class UserImformation():
    def __init__(self):
        self.employ = 'employee'
        self.db = DbOperate()

    def count_user(self):
        result = self.db.list_sum(self.employ)
        return result

#偷懒后遗症
    def return_all_user(self):
        count = self.db.list_sum(self.employ)
        list = []
        index = 0
        allUser = self.db.get_all_user()
        print("all_user:", allUser)
        while(index < count):

            data = {'name': allUser[index][1],
                    'identity': allUser[index][0]
                    }

            list.append(data)
            index = index +1

        return list

    #def return_page_user(self, ):

def delete_floder(path):  #删除该路径以及所有内部所有文件
    for filename in os.listdir(path):
        a_path = os.path.join(path, filename)
        if os.path.isfile(a_path) or os.path.islink(a_path):
            os.unlink(a_path)
        elif os.path.isdir(a_path):
            shutil.rmtree(a_path)
    os.rmdir(path)


def delete_user(id):
    db = DbOperate()
    flag = db.delete_employee(id)    #数据库删除
    path = "faces/"+str(int(id)-1)   #别忘了-1
    print(path)
    #flag为则Ture 数据库无该数据 返回Ture 数据不存在
    if flag:
        return flag
    else:
        delete_floder(path)

def train_model():
    train_the_model("faces")

#状态类我不懂所以前端一次性发全部的内容，这部分注释掉了
# globalState = {}
# mutex = threading.Lock()
#
# class State(object):
#     def __init__(self, name, id):
#         self.name = name
#         self.id = id
#         self.imgs = []
#
#     def addImg(self, img):
#         self.imgs.append(img)
#
#
# def getContext(name:str, id:int):
#     id = uuid4()
#     mutex.locked()
#     globalState[id] = State(name, id)
#     mutex.release()
#     return id
#
# def addImage(id:UUID, image):
#     mutex.locked()
#     state = globalState[id]
#     state.addImg(image)
#     mutex.release()
#
# def closeContext(id:UUID):
#     mutex.locked()
#     del globalState[id]
#     mutex.release()
