from datetime import datetime

import numpy as np

from FaceRecognition.FaceCollect import faceCollect
from FaceRecognition.FeatureCompute import featureCompute


class Person:
    # 公有变量
    name: str  # 姓名
    id: int  # 编号
    record: dict  # 记录[日期, 记录(签到/签退)]

    # 私有变量
    __faceInfo: np.array  # 人脸信息

    def __init__(self, _name: str, _id: int, _record=None, _faceInfo=None):
        self.name = _name
        self.id = _id
        self.__faceInfo = _faceInfo
        self.record = _record if _record is not None else {}

    def SetFaceInfo(self, camera):  # 采集人脸信息, 并存储到数据库
        name, faceImageList = faceCollect.GetFaceListFromVideo(self.name, camera)
        # faceCollect.StorageFaceImageList(name, faceImageList)
        self.__faceInfo = featureCompute.GetMeanFeature(faceImageList)
        featureCompute.SaveFeatureToSql([[name, list(self.__faceInfo)]])

    def SignIn(self):  # 签到
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now().strftime('%H:%M:%S')
        if today not in self.record:
            self.record[today] = []
        self.record[today].append(now + '--签到')

    def SignOut(self):  # 签退
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now().strftime('%H:%M:%S')
        if today not in self.record:
            self.record[today] = []
        self.record[today].append(now + '--签退')

    def printInfo(self):
        print('Name:', self.name)
        print('ID:', self.id)
        print('Record:\n', self.recordToString(), sep='')

    def recordToString(self):
        if len(self.record) == 0:
            return '无记录'
        ret = ''
        for date, record in self.record.items():
            ret += date + ':\t'
            for r in record:
                ret += r + '\t'
            ret += '\n'
        return ret

    def SignInWithTime(self, day, time):
        if day not in self.record:
            self.record[day] = []
        if time + '--签到' not in self.record[day]:
            self.record[day].append(time + '--签到')

    def SignOutWithTime(self, day, time):
        if day not in self.record:
            self.record[day] = []
        if time + '--签退' not in self.record[day]:
            self.record[day].append(time + '--签退')


if __name__ == '__main__':
    pass



