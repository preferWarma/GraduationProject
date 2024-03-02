import os
import re

import cv2
import numpy as np

from Config import config


class FeatureCompute:
    # 私有属性
    # 共有属性

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

    def SaveFeature(self, featureStructList: list, isAppend: bool = True):
        """
        保存特征列表
        :param isAppend: 是否以追加的方式保存
        :param featureStructList: 特征结构体列表, 结构体的第一个元素为人名, 第二个元素为特征列表
        """
        if not os.path.exists(config.featureSaveFolderRoot):
            os.makedirs(config.featureSaveFolderRoot)
        savePath = os.path.join(config.featureSaveFolderRoot, "meanFeature.csv")

        if isAppend:
            with open(savePath, "w") as f:
                for name, feature in featureStructList:
                    f.write(name + "," + str(feature) + "\n")
        else:
            with open(savePath, "a") as f:
                for name, feature in featureStructList:
                    f.write(name + "," + str(feature) + "\n")


featureCompute = FeatureCompute()  # 创建特征计算对象, 供其他模块使用

if __name__ == '__main__':  # 测试代码
    featureStructList = []
    for name in os.listdir(config.imageSaveFolderRoot):
        imageList = featureCompute.GetImageList(os.path.join(config.imageSaveFolderRoot, name))
        meanFeature = featureCompute.GetMeanFeature(imageList)
        print(f"{name}的特征均值为{list(meanFeature)}\n")
        featureStructList.append((name, list(meanFeature)))
    featureCompute.SaveFeature(featureStructList)
