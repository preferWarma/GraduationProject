from datetime import datetime, timedelta

from FaceRecognition.FaceCollect import faceCollect
from FaceRecognition.FeatureCompute import featureCompute


class Person:
    def __init__(self, _name: str, _id: int, _record=None, _faceInfo=None):
        self.name = _name
        self.id = _id
        self.faceInfo = _faceInfo
        self.record = _record if _record is not None else {}

    def SetFaceInfo(self, camera):  # 采集人脸信息, 并存储到数据库
        faceImageList = faceCollect.GetFaceListFromVideo(camera)
        # faceCollect.StorageFaceImageList(name, faceImageList)
        self.faceInfo = featureCompute.GetMeanFeature(faceImageList)
        featureCompute.SaveFeatureToSql([[self.name, list(self.faceInfo)]])

    def SignIn(self) -> bool:  # 签到
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now()
        if today not in self.record:
            self.record[today] = []

        # 检查是否有签到记录，并且距离上次签到时间是否超过0.5小时
        lastSignInTime = self.getLastSignInTime(today)
        if lastSignInTime is None or (now - lastSignInTime) > timedelta(hours=0.5):
            self.record[today].append(now.strftime('%H:%M:%S') + '--签到')
            return True
        else:
            print("半小时内只能签到一次")
            return False

    def SignOut(self) -> bool:  # 签退
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now()
        if today not in self.record:
            self.record[today] = []
        # 检查是否有签退记录，并且距离上次签退时间是否超过0.5小时
        lastSignOutTime = self.getLastSignOutTime(today)
        if lastSignOutTime is None or (now - lastSignOutTime) > timedelta(hours=0.5):
            self.record[today].append(now.strftime('%H:%M:%S') + '--签退')
            return True
        else:
            print("半小时内只能签退一次")
            return False

    def getLastSignInTime(self, today):
        if today in self.record.keys():
            for record in reversed(self.record[today]):
                if '签到' in record:
                    return datetime.strptime(today + ' ' + record.split('--')[0], '%Y-%m-%d %H:%M:%S')
        return None

    def getLastSignOutTime(self, today):
        if today in self.record and self.record[today]:
            for record in reversed(self.record[today]):
                if '签退' in record:
                    return datetime.strptime(today + ' ' + record.split('--')[0], '%Y-%m-%d %H:%M:%S')
        return None

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
    p = Person('test', 1)
    p.printInfo()
    p.SignIn()
    p.SignIn()
    p.SignOut()
    p.SignOut()
    p.printInfo()
