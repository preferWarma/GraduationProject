import os
import random
import cv2
import dlib

output_dir = 'D:\\Projects\\PytorchProject\\Image\\Cjh'  # 存储位置
size = 64  # 图像大小

# 如果没有这个文件夹就创建
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def relight(img, light=1.0, bias=0):
    """
    改变图片的亮度与对比度

    Parameters:
    - img: 输入图像
    - light: 亮度因子
    - bias: 对比度偏移量

    Returns:
    - img: 处理后的图像
    """
    w = img.shape[1]  # 图像宽度
    h = img.shape[0]  # 图像高度
    for i in range(0, w):
        for j in range(0, h):
            for c in range(3):  # 对应BGR三个通道
                tmp = int(img[j, i, c] * light + bias)  # 亮度计算, 限制在0-255
                if tmp > 255:
                    tmp = 255
                elif tmp < 0:
                    tmp = 0
                img[j, i, c] = tmp
    return img


# 使用dlib自带的frontal_face_detector作为我们的特征提取器
detector = dlib.get_frontal_face_detector()

# 打开摄像头 参数为输入流，可以为摄像头或视频文件
camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture('D:\\Projects\\PytorchProject\\Video\\test.mp4')

index = 1
while index <= 20:  # 存储20张人脸特征图像
    print('Being processed picture %s' % index)
    # 从摄像头读取照片
    success, img = camera.read()
    # 转为灰度图片
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用detector进行人脸检测, 1表示使用单层图像金字塔
    faces = detector(gray_img, 1)  # 返回的是所有人脸的矩形框(用于定位人脸)

    for i, d in enumerate(faces):  # 对每个人脸都进行处理, i为矩形框索引, d为人脸的矩形框
        x1 = d.top() if d.top() > 0 else 0
        y1 = d.bottom() if d.bottom() > 0 else 0
        x2 = d.left() if d.left() > 0 else 0
        y2 = d.right() if d.right() > 0 else 0

        face = img[x1:y1, x2:y2]  # 截取脸部图像
        face = relight(face, random.uniform(0.8, 1.2), random.randint(-50, 50))  # 调整图片的对比度与亮度， 对比度与亮度值都取随机数，这样能增加样本的多样性
        face = cv2.resize(face, (size, size))  # 调整图片的尺寸
        cv2.imshow('image', face)  # 显示图片
        # 图片存储路径以及图片名为 {output_dir}/{dirName}_{index}.jpg
        cv2.imwrite(os.path.join(output_dir, os.path.basename(output_dir) + f'_{index}.png'), face)  # 存储图片

        index += 1

    key = cv2.waitKey(30) & 0xff    # 获取键盘输入, 30ms延时
    if key == 27:   # 按ESC键可以提前强制退出
        break

print('Finished!')
# 释放摄像头 release camera
camera.release()
# 删除建立的窗口 delete all the windows
cv2.destroyAllWindows()
