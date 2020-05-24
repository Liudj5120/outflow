#批量修改文件名
#批量修改图片文件名
import os
import re
import sys
def renameall(path):
    fileList = os.listdir(path) #待修改文件夹
    print("修改前：" + str(fileList))   #输出文件夹中包含的文件
    currentpath = os.getcwd()   #得到进程当前工作目录
    os.chdir(path)
    for fileName in fileList:
        if 'mydata' in fileName and '.bur' in fileName:
            temp = fileName.split('data')
            os.rename(fileName, temp[1])    #文件重新命名
        else:
            continue
    os.chdir(currentpath)   #改回程序运行前的工作目录
    sys.stdin.flush()   #刷新
def main():
    path = 'E:/zi'
    renameall(path)
   
if __name__ == '__main__':
    main()