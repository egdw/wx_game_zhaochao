import os

import cv2 as cv
import imutils
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pygame

# 获取截图
def pull_screenshot():
    os.system('/Users/hdy/Library/Android/sdk/platform-tools/adb shell screencap -p /sdcard/autodect.png')
    os.system('/Users/hdy/Library/Android/sdk/platform-tools/adb pull /sdcard/autodect.png .')

# 模拟点击
def click(location):
    cmd = '/Users/hdy/Library/Android/sdk/platform-tools/adb shell input tap ' + str(location[0]) + " " + str(
        location[1])
    os.system(cmd)

# 设置窗体和大小
cv.namedWindow("result",0)
cv.resizeWindow("result",400,400)
# 开始事件
def start():
    global times
    fig = plt.figure()
    # 获取截图
    pull_screenshot()
    # 打开图片
    im = np.array(Image.open('autodect.png'))
    # 这里我没有自动判断坐标.需要根据自己手机设置一下找茬上下两张图的坐标
    # pic1(y1,y2,x1,x2) (x1,y1)为左上角的坐标点 (x2,y2)为第一张图的右下角的点
    # pic2(y1,y2,x1,x2) (x1,y1)为左上角的坐标点 (x2,y2)为第一张图的右下角的点
    pic1 = im[143:921, 199:1023]
    # 注意!!!.后面的199:1023 的值上下必须一样!根据你的机子进行修改
    pic2 = im[1043:1821, 199:1023]
    # 判断两张地图的不同
    t = cv.absdiff(pic1, pic2)
    # 模糊
    t = cv.blur(t, (5, 5))
    # 转换为灰度图
    t = cv.cvtColor(t, cv.COLOR_BGR2GRAY)
    # 五次闭运算,用于去除部分噪点
    for i in range(5):
        kernel = np.uint8(np.zeros((5, 5)))
        for x in range(5):
            kernel[x, 2] = 1;
            kernel[2, x] = 1;
        # 膨胀
        t = cv.dilate(t, kernel)
        kernel = np.uint8(np.zeros((5, 5)))
        for x in range(5):
            kernel[x, 2] = 1;
            kernel[2, x] = 1;
        # 腐蚀
        t = cv.erode(t, kernel)
    # 进行高斯模糊
    t = cv.GaussianBlur(t, (5, 5), 1.5)
    # 找轮廓
    cnts = cv.findContours(t.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    for c in cnts:
        (x, y, w, h) = cv.boundingRect(c)
        # 排除掉不符合的轮廓
        if w > 20 and h > 20 and w < 300 and h < 300:
            # 找到相应的坐标
            # (199)这里是上面pic1中的x1的值
            l_x = (x + w / 2) + 199
            # 这里(143)是h的值.计算请看图片
            l_y = (y + h / 2) + 143
            location = [l_x, l_y]
            # 把茬点用框框框出来
            cv.rectangle(pic1, (x, y), (x + w, y + h), (0, 0, 255), 3)
            # 模拟点击坐标
            click(location)
    cv.namedWindow("result", 0)
    cv.resizeWindow("result", 400, 400)
    cv.imshow("result", pic1)
    cv.waitKey(0)
    cv.destroyAllWindows()
    start()


pygame.init()
while True:
    for event in pygame.event.get():
        if event.type == 2:
            # 按空格键开始计算
            start()