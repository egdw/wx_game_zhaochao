# wx_game_zhaochao
微信小程序找茬外挂

## 实际效果
![演示界面](https://raw.githubusercontent.com/egdw/wx_game_zhaochao/master/%E5%8A%A8%E7%94%BB.GIF)
注意目前只能完成一个图片重新点击一次空格再识别一次.

## 基于opencv和python3的微信小程序找茬外挂
注意电脑上需要安装好opencv并且安装好opencv_python,然后才可以使用

```
pip install --upgrade setuptools
pip install numpy Matplotlib
pip install opencv-python
# 以上是pip安装opencv-python的方法
# 电脑上还需要安装opencv的库才可以使用
```

## 设备需要开启开发者模式!

## 原理说明
1. 将手机点击到《大家来找茬》小程序界面

2. 用 ADB 工具获取当前手机截图，并用 ADB 将截图 pull 上来
```shell
adb shell screencap -p /sdcard/autodect.png
adb pull /sdcard/autodect.png .
```

3. 截取图片计算区别点
  保存坐标中心点

4. 用 ADB 工具点击屏幕蓄力一跳
```shell
adb input tap x y
```

## 相关设置

### 第一处设置
![坐标设置](https://raw.githubusercontent.com/egdw/wx_game_zhaochao/master/tip2.png)

```
    # 这里我没有自动判断坐标.需要根据自己手机设置一下找茬上下两张图的坐标
    # pic1(y1,y2,x1,x2) (x1,y1)为左上角的坐标点 (x2,y2)为第一张图的右下角的点
    # pic2(y1,y2,x1,x2) (x1,y1)为左上角的坐标点 (x2,y2)为第一张图的右下角的点
    pic1 = im[143:921, 199:1023]
    # 注意!!!.后面的199:1023 的值上下必须一样!根据你的机子进行修改
    pic2 = im[1043:1821, 199:1023]
```
### 第二处设置

![高度设置](https://raw.githubusercontent.com/egdw/wx_game_zhaochao/master/tip1.png)
```
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
```

### 第三处设置
修改adb路径指向为你的路径
```
# 模拟点击
def click(location):
    # 请在这里设置你的adb路径
    cmd = '/Users/hdy/Library/Android/sdk/platform-tools/adb shell input tap ' + str(location[0]) + " " + str(
        location[1])
    os.system(cmd)
```
## 识别效果图
![效果图1](https://raw.githubusercontent.com/egdw/wx_game_zhaochao/master/result1.png)
![效果图2](https://raw.githubusercontent.com/egdw/wx_game_zhaochao/master/result2.png)
![效果图3](https://raw.githubusercontent.com/egdw/wx_game_zhaochao/master/result3.png)
![效果图4](https://raw.githubusercontent.com/egdw/wx_game_zhaochao/master/result4.png)
