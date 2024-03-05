import time

import cv2

from AttendanceSystem.Person import Person
from SqlController import sqlController


class Manager:
    def __init__(self):
        pass

    def AddPerson(self, _name, camera) -> Person:  # 添加人员, 并返回添加的Person对象
        p = Person(_name, sqlController.GetNewId())
        p.SetFaceInfo(camera)
        sqlController.InsertPersonWithJudgeExist(p.id, p.name, p.record)
        return p

    def DeletePerson(self, _id: int):
        p = self.GetPerson(_id)
        if p is None:
            return
        sqlController.DeletePerson(p.id)
        sqlController.Delete(p.name)

    def UpdatePerson(self, _id, _name, _record: dict):
        sqlController.UpdatePerson(_id, _name, _record)

    def GetPerson(self, _id: int):
        res = sqlController.SelectPerson(_id)
        if res is None:
            return None
        return Person(res[0], _id, res[1])


manager = Manager()


def test1():
    p = manager.GetPerson(2)
    p.printInfo()
    p.name = 'ZhangSan'
    p.SignIn()
    time.sleep(3)
    p.SignOut()
    manager.UpdatePerson(p.id, p.name, p.record)
    p = manager.GetPerson(2)
    p.printInfo()


def test2():
    p = manager.AddPerson('LiSi', cv2.VideoCapture(0))
    p.printInfo()
    manager.DeletePerson(1)
    p = manager.GetPerson(1)
    if p is None:
        print('删除成功')
    else:
        p.printInfo()


def test3():
    p = manager.GetPerson(1)
    p.printInfo()
    p.SignIn()
    time.sleep(3)
    p.SignOut()
    manager.UpdatePerson(p.id, p.name, p.record)
    p = manager.GetPerson(1)
    p.printInfo()


if __name__ == '__main__':
    p = manager.GetPerson(1)
    p.printInfo()
    # 在昨天的记录上签到
    p.SignInWithTime('2021-07-20', '08:00:00')
    p.SignOutWithTime('2021-07-20', '17:00:00')
    manager.UpdatePerson(p.id, p.name, p.record)
    p = manager.GetPerson(1)
    p.printInfo()
