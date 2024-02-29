import os

import dlib


class Config:
    # 私有属性
    # 人脸关键点检测模型的路径
    __shapePredictorPath: str = 'D:\\Projects\\PytorchProject\\Models\\shape_predictor_68_face_landmarks.dat'
    # Dlib 人脸识别模型路径
    __faceRecognitionModelPath: str = 'D:\\Projects\\PytorchProject\\Models\\dlib_face_recognition_resnet_model_v1.dat'

    # 共有属性
    imageSize: int = 64  # 采集的图像大小
    threshold: float = 0.5  # 人脸相似度阈值
    captureImageCount: int = 10  # 采集图像数量

    imageSaveFolderRoot: str = 'D:\\Projects\\PytorchProject\\Image'  # 图像存储位置根目录
    featureSaveFolderRoot: str = 'D:\\Projects\\PytorchProject\\Csv'  # CSV 文件存储位置根目录

    detector = dlib.get_frontal_face_detector()  # 人脸检测器
    predictor = dlib.shape_predictor(__shapePredictorPath)  # 人脸关键点检测器
    faceRecognitionModel = dlib.face_recognition_model_v1(__faceRecognitionModelPath)  # 人脸识别模型

    def __init__(self):
        print("初始化配置信息")
        if not os.path.exists(self.imageSaveFolderRoot):
            os.makedirs(self.imageSaveFolderRoot)
        if not os.path.exists(self.featureSaveFolderRoot):
            os.makedirs(self.featureSaveFolderRoot)
        if not os.path.exists(self.__shapePredictorPath):
            print("人脸关键点检测模型路径不存在")
        if not os.path.exists(self.__faceRecognitionModelPath):
            print("人脸识别模型路径不存在")


config = Config()  # 创建配置对象, 供其他模
# 块使用

if __name__ == '__main__':
    pass
