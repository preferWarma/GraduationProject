import os
import random

import cv2
import numpy

from Config import config


class FaceCollect:
    # 私有属性
    _camera = cv2.VideoCapture(0)  # 打开摄像头 参数为输入流，可以为摄像头或视频文件, 0表示第一个摄像头
    _captureImageCount: int  # 存储人脸特征图像张数

    def __init__(self, videoPath: str = None, captureImageCount: int = config.captureImageCount):
        if videoPath is not None:
            self._camera = cv2.VideoCapture(videoPath)
        self._captureImageCount = captureImageCount

    # 共有方法
    def GetFaceList(self, _name: str):
        """
        采集人脸数据
        :return: 人名以及对应的人脸图像列表
        """
        faceImageList = []
        while True:  # 采集captureImageCount张人脸图像
            success, image = self._camera.read()
            faces = config.detector(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 1)  # 返回的是所有人脸的矩形框(用于定位人脸)
            if len(faces) > 1:
                print("检测到多张人脸, 请保持画面上只有一张人脸")
                continue
            elif len(faces) == 0:
                print("未检测到人脸, 请保持画面上有一张人脸")
                continue
            rectangle = faces[0]
            x1 = rectangle.top() if rectangle.top() > 0 else 0
            y1 = rectangle.bottom() if rectangle.bottom() > 0 else 0
            x2 = rectangle.left() if rectangle.left() > 0 else 0
            y2 = rectangle.right() if rectangle.right() > 0 else 0
            faceImage = image[x1:y1, x2:y2]  # 截取人脸

            cv2.imshow('image', faceImage)  # 显示图片
            if cv2.waitKey(1) & 0xFF == ord('q'):   # 如果不延迟, 会造成显示不正常
                break

            # 随机化亮度与对比度
            faceImage = self.__RandomizeImage(faceImage, random.uniform(0.8, 1.2), random.randint(-50, 50))
            # 调整图片的尺寸
            faceImage = cv2.resize(faceImage, (config.imageSize, config.imageSize))
            faceImageList.append(faceImage)

            if len(faceImageList) > self._captureImageCount:
                break
        cv2.destroyAllWindows()
        return _name, faceImageList

    def StorageFaceImageList(self, _name: str, faceImageList: list):
        """
        存储人脸图像列表
        :param _name: 人脸图像列表对应的人名
        :param faceImageList: 人脸图像列表
        """
        folderPath = os.path.join(config.imageSaveFolderRoot, _name)
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        for index, faceImage in enumerate(faceImageList):
            cv2.imwrite(os.path.join(folderPath, f"{_name}_{index}.png"), faceImage)

    # 私有方法
    def __RandomizeImage(self, image: numpy.ndarray, light: float, bias: int) -> numpy.ndarray:
        """
        改变图片的亮度与对比度
        :param image: 需要处理的图像
        :param light: 亮度因子
        :param bias: 对比度偏移量
        :return: 处理后的图像
        """
        width = image.shape[1]  # 图像宽度
        height = image.shape[0]  # 图像高度
        for i in range(width):
            for j in range(height):
                for c in range(3):  # 对应BGR三个通道
                    tmp = int(image[j, i, c] * light + bias)
                    if tmp > 255:
                        tmp = 255
                    elif tmp < 0:
                        tmp = 0
                    image[j, i, c] = tmp
        return image


faceCollect = FaceCollect()  # 创建人脸采集对象, 供其他模块使用

if __name__ == '__main__':  # 测试代码
    name, faceList = faceCollect.GetFaceList("Cjy")
    for face in faceList:
        cv2.imshow('image', face)  # 显示图片
        cv2.waitKey(0)  # 等待按键 0 表示无限等待
        cv2.destroyAllWindows()
    faceCollect.StorageFaceImageList(name, faceList)
