import os
import re

import cv2
import numpy as np

from Config import config


class FeatureCompute:
    def __init__(self):
        pass

    def GetFaceFeature(self, Image: np.ndarray) -> np.array:
        """
        提取人脸关键点
        :param Image: 需要提取的图像
        :return: 人脸特征128D向量
        """
        GrayImage = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
        faces = config.detector(GrayImage, 1)  # 定位人脸, 返回的是所有人脸信息的列表
        if len(faces) == 0:
            print("此照片未检测到人脸, 请重新选择照片")
            return None
        elif len(faces) > 1:
            print("检测到多张人脸, 请重新选择照片, 保持画面上只有一张人脸, 以防止其他人脸的干扰")
            return None
        else:
            landmark = config.predictor(Image, faces[0])  # 提取人脸关键点
            feature = config.faceRecognitionModel.compute_face_descriptor(Image, landmark)  # 提取人脸特征
            return np.array(feature)

    def GetFaceFeatureList(self, ImageList: list) -> list:
        """
        提取人脸关键点列表
        :param ImageList: 需要提取的图像列表
        :return: 人脸关键点列表
        """
        featureList = []
        for Image in ImageList:
            Feature = self.GetFaceFeature(Image)
            if Feature is not None:
                featureList.append(Feature)
        return featureList

    def GetMeanFeature(self, ImageList: list) -> np.array:
        """
        计算人脸特征的均值
        :param ImageList: 图像列表
        :return: 人脸特征的均值
        """
        featureList = self.GetFaceFeatureList(ImageList)
        return np.array(featureList).mean(axis=0)

    def GetImageList(self, ImageFolderPath: str) -> list:
        """
        获取图像列表
        :param ImageFolderPath: 图像文件夹路径
        :return: 图像列表
        """
        imageList = []
        # 读取该文件夹下的所有人脸图像
        photosList = os.listdir(ImageFolderPath)
        if not photosList:
            print("文件夹内图像文件为空 / Warning: No images in " + ImageFolderPath + '\n')
            return imageList
        # 按照文件名中的数字排序
        photosList = sorted(photosList, key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
        for photoName in photosList:
            curImagePath = os.path.join(ImageFolderPath, photoName)
            imageList.append(cv2.imread(curImagePath))
        return imageList


featureCompute = FeatureCompute()  # 创建特征计算对象, 供其他模块使用
