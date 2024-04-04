import os

import cv2
import numpy as np

from Config import config


class FaceCollect:
    # 私有属性

    def __init__(self, captureImageCount: int = config.captureImageCount):
        self.captureImageCount = captureImageCount

    # 共有方法
    def GetFaceListFromVideo(self, camera):
        """
        采集人脸数据
        :return: 人名以及对应的人脸图像列表
        """
        faceImageList = []
        while True:  # 采集captureImageCount张人脸图像
            success, image = camera.read()
            faces = config.detector(self.PreHandleImage(image), 1)  # 返回的是所有人脸的矩形框(用于定位人脸)
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

            # cv2.imshow('image', faceImage)  # 显示图片
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 如果不延迟, 会造成显示不正常
                break

            # 调整图片的尺寸
            faceImage = cv2.resize(faceImage, (config.imageSize, config.imageSize))
            faceImageList.append(faceImage)

            if len(faceImageList) > self.captureImageCount:
                break
        cv2.destroyAllWindows()
        return faceImageList

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
    def PreHandleImage(self, image):
        """
        对图像进行预处理
        :return: 处理后的图像
        """
        # 灰度化
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 直方图均衡化
        image = cv2.equalizeHist(image)
        # 高斯滤波
        image = cv2.GaussianBlur(image, (5, 5), 0)
        # 转为8bit灰度图像, 供dlib检测器使用
        image = image.astype(np.uint8)

        return image

    def __del__(self):
        cv2.destroyAllWindows()


faceCollect = FaceCollect()  # 创建人脸采集对象, 供其他模块使用
