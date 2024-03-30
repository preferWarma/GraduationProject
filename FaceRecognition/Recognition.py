import time

import cv2
import numpy as np

from Config import config
from SqlController import sqlController


class Recognition:
    def __init__(self):
        self.knownFeatureList = sqlController.SelectAllFaceInfo()

    def __GetEuclideanDistance(self, feature1, feature2) -> float:
        """
        计算欧式距离
        :param feature1: 特征1
        :param feature2: 特征2
        :return: 两个特征之间的欧式距离
        """
        return np.sqrt(np.sum(np.square(np.array(feature1) - np.array(feature2))))

    def __DetectFaces(self, image, detector):
        """
        检测图像中的人脸
        :param image: 每一帧的输入图像
        :param detector: 人脸检测器
        :return: faces: 检测到的人脸列表
        """
        if image is None:
            return []
        grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        faces = detector(grayImage, 0)
        return faces

    def __DrawRectangleAndText(self, image, faceList, faceFeatureList):
        font = cv2.FONT_HERSHEY_COMPLEX  # 字体
        for index, face in enumerate(faceList):
            name = faceFeatureList[index][0]
            # 绘制矩形框
            rectanglePosition = tuple([face.left(), face.top(), face.right(), face.bottom()])  # 矩形框位置
            rectangleColor = (0, 255, 0)  # 矩形框颜色: 绿色
            cv2.rectangle(image, rectanglePosition[0:2], rectanglePosition[2:], rectangleColor, 2)
            # 绘制文字
            textPosition = tuple([face.left(), int(face.bottom() + (face.bottom() - face.top()) / 4)])  # 文字位置
            textColor = (0, 255, 0) if name != "unknown" else (0, 0, 255)  # 如果是已知人脸显示颜色为绿色, 否则为红色
            cv2.putText(image, name, textPosition, font, 1, textColor, 2)

    def Main(self, camera):

        while camera.isOpened():
            start_time = time.time()

            success, frame = camera.read()
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

            frame, _, faceList = self.handle(frame)  # 处理每一帧
            # 显示当前帧中人脸数量
            cv2.putText(frame, "VisitorNumber: " + str(len(faceList)), (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.imshow("camera", frame)

            end_time = time.time()
            elapsed_time = end_time - start_time
            fps = 1 / elapsed_time
            print(f"FPS: {fps}")

        camera.release()
        cv2.destroyAllWindows()

    def handle(self, frame):
        """
        处理每一帧， 识别人脸并在图像中标出人脸位置和姓名
        :param frame: 帧图像
        :return: 返回处理后的图像和识别到的成员名字
        """
        faceList = self.__DetectFaces(frame, config.detector)
        retInfoList = []  # 识别到的人脸信息列表[(id, name), ...]
        if not faceList:
            return frame, retInfoList, faceList

        faceFeatureList = []  # 当前帧的人脸特征列表,格式[name, feature(128D)]
        for face in faceList:
            landmark = config.predictor(frame, face)
            feature = config.faceRecognitionModel.compute_face_descriptor(frame, landmark)
            faceFeatureList.append(["unknown", feature])

        for faceFeature in faceFeatureList:
            # 在数据库中查找与当前人脸最相似的人脸
            minDistance = 1e9
            similarPerson = None
            for knownFeature in self.knownFeatureList:  # knownFeatureList: [[id, name, feature(128D)], ...]
                distance = self.__GetEuclideanDistance(faceFeature[1], knownFeature[2])
                if distance < minDistance and distance < config.threshold:
                    minDistance = distance
                    similarPerson = knownFeature
            if similarPerson is not None:
                faceFeature[0] = f"{similarPerson[0]}: {similarPerson[1]}"  # 显示id和姓名
                retInfoList.append((similarPerson[0], similarPerson[1]))

        self.__DrawRectangleAndText(frame, faceList, faceFeatureList)
        return frame, retInfoList, faceList


recognition = Recognition()  # 创建识别对象, 供其他模块使用

if __name__ == '__main__':  # 测试运行
    recognition.Main(cv2.VideoCapture(0))
    pass
