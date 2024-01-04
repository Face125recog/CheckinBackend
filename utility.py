import os
import re
import sys

def RenameAllFirst(floder):
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

def RenameAllLast(floder):
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


def LastFileNum(floderPath):
    if os.path.exists(floderPath):
        file_count = len(os.listdir(floderPath))
        return file_count
    else:
        return 0