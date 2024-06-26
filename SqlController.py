from datetime import datetime
from typing import Optional

import mysql.connector
import numpy as np

from AttendanceSystem.Employee import AttendanceRecord, User


class SqlController:
    def __init__(self, host="localhost", user="root", passwd="Aa112211", database="graduation"):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )  # 连接数据库
        self.cursor = self.db.cursor()  # 创建游标

    def SelectEmployeeBaseInfoById(self, EmployeeID):
        sql = "select * from employees where EmployeeID = %s"
        self.cursor.execute(sql, (EmployeeID,))
        result = self.cursor.fetchone()
        return result

    def SelectEmployeeBaseInfoByName(self, EmployeeName):
        sql = "select * from employees where Name = %s"
        self.cursor.execute(sql, (EmployeeName,))
        result = self.cursor.fetchone()
        return result

    def SelectAllFaceInfo(self):
        """
        查询所有员工的人脸信息
        :return: [[EmployeeID, EmployeeName, Face_Info], ...]的信息列表
        """
        sql = "select * from faceinfo"
        self.cursor.execute(sql)
        selectResult = self.cursor.fetchall()
        if selectResult is None:
            return []
        ret = []  # 返回值格式为[[EmployeeID, EmployeeName, Face_Info], ...]
        for result in selectResult:
            ret.append([result[0], result[1], np.fromstring(result[2][1:-1], sep=', ')])
        return ret

    def SelectAttendanceRecordByEmployeeID(self, EmployeeID):
        sql = "select * from attendance where EmployeeID = %s"
        self.cursor.execute(sql, (EmployeeID,))
        sqlResult = self.cursor.fetchall()
        # 将查询结果转换为AttendanceRecord对象(签到时间, 签到状态)
        ret = []
        for result in sqlResult:
            ret.append(AttendanceRecord(result[0], result[1], result[2], result[3]))
        return ret

    def SelectAttendanceRecordByRecordID(self, RecordID):
        sql = "select * from attendance where AttendanceID = %s"
        self.cursor.execute(sql, (RecordID,))
        result = self.cursor.fetchone()
        # 将查询结果转换为AttendanceRecord对象(签到时间, 签到状态)
        return AttendanceRecord(result[0], result[1], result[2], result[3]) if result is not None else None

    def InsertEmployee(self, name, position, salary, age, gender):
        sql = "INSERT INTO employees (Name, Position, Salary, Age, Gender) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (name, position, int(salary), int(age), 0 if gender == "男" else 1))
        self.db.commit()
        return self.cursor.lastrowid  # 返回插入的ID

    def InsertAttendanceRecord(self, EmployeeID, AttendanceDateTime, AttendanceType):
        # INSERT INTO attendance (EmployeeID, AttendanceDateTime, AttendanceType) VALUES (9, '2024-03-30 23:05:39', 0)
        sql = "INSERT INTO attendance (EmployeeID, AttendanceDateTime, AttendanceType) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (EmployeeID, AttendanceDateTime, AttendanceType))
        self.db.commit()

    def DeleteEmployee(self, EmployeeID):
        sql = "delete from employees where EmployeeID = %s"
        self.cursor.execute(sql, (EmployeeID,))
        self.db.commit()

    def DeleteAttendanceRecordByEmployeeID(self, EmployeeID):
        sql = "delete from attendance where EmployeeID = %s"
        self.cursor.execute(sql, (EmployeeID,))
        self.db.commit()

    def DeleteAttendanceRecordByRecordId(self, AttendanceID):
        sql = "delete from attendance where AttendanceID = %s"
        self.cursor.execute(sql, (AttendanceID,))
        self.db.commit()

    def UpdateEmployeeFaceInfo(self, EmployeeID, faceInfo):
        # 更新数据库
        sql = "update faceinfo set Face_Info = %s where EmployeeID = %s"
        self.cursor.execute(sql, (str(list(faceInfo)), EmployeeID))
        self.db.commit()
        return faceInfo

    def UpdateEmployeeBaseInfo(self, id, name, position, salary, age, gender):
        # 更新人员的基本信息
        sql = "UPDATE employees SET Name = %s, Position = %s, Salary = %s, Age = %s, Gender = %s WHERE EmployeeID = %s"
        self.cursor.execute(sql, (name, position, salary, age, gender, id))
        self.db.commit()

    def UpdateUserPassword(self, userId, newPassword):
        sql = "update user set Password = %s where userID = %s"
        self.cursor.execute(sql, (newPassword, userId))
        self.db.commit()

    def UpdateUserType(self, userId, userType: int):    # 0: 员工, 1: 管理员
        sql = "update user set UserType = %s where userID = %s"
        self.cursor.execute(sql, (userType, userId))
        self.db.commit()

    def Login(self, idOrName: str, password: str) -> Optional[User]:
        sql = "select * from user where userID = %s and Password = %s"
        self.cursor.execute(sql, (idOrName, password))
        result = self.cursor.fetchone()
        if result is not None:
            return User(result[0], result[1], result[2])
        else:  # 编号查询不到，尝试姓名查询
            _info = sqlController.SelectEmployeeBaseInfoByName(idOrName)
            if _info is None:
                return None
            _id = _info[0]
            sql = "select * from user where userID = %s and Password = %s"
            self.cursor.execute(sql, (_id, password))
            result = self.cursor.fetchone()
            if result is not None:
                return User(result[0], result[1], result[2])
        return None

    def SignIn(self, EmployeeID):
        now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.InsertAttendanceRecord(EmployeeID, now_datetime, 0)

    def SignOut(self, EmployeeID):
        now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.InsertAttendanceRecord(EmployeeID, now_datetime, 1)

    def GetLastSignInTime(self, EmployeeID) -> Optional[datetime]:
        """
        获取最后一次签到时间, 返回的是None或者datetime
        """
        sql = ("select * from attendance where EmployeeID = %s and AttendanceType = 0 "
               "order by AttendanceDateTime desc limit 1")
        self.cursor.execute(sql, (EmployeeID,))
        result = self.cursor.fetchone()  # 返回的是一个元组(AttendanceID, EmployeeID, AttendanceDateTime, AttendanceType)
        if result is None:
            return None
        return result[2]

    def GetLastSignOutTime(self, EmployeeID) -> Optional[datetime]:
        """
        获取最后一次签退时间, 返回的是None或者datetime
        """
        sql = ("select * from attendance where EmployeeID = %s and AttendanceType = 1 "
               "order by AttendanceDateTime desc limit 1")
        self.cursor.execute(sql, (EmployeeID,))
        result = self.cursor.fetchone()  # 返回的是一个元组(AttendanceID, EmployeeID, AttendanceDateTime, AttendanceType)
        if result is None:
            return None
        return result[2]

    def ExecuteWithSql(self, sql: str):
        self.cursor.execute(sql)  # 执行sql语句
        self.db.commit()  # 提交事务

    def SelectWithSql(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def __del__(self):
        self.db.close()


sqlController = SqlController()

if __name__ == '__main__':
    info = sqlController.SelectEmployeeBaseInfoByName("lyf")
    print(info)  # info = (EmployeeID, Name, Position, Salary, Age, Gender)
    attendanceList = sqlController.SelectAttendanceRecordByEmployeeID(info[0])
    for record in attendanceList:
        print(str(record))
    last_in = sqlController.GetLastSignInTime(info[0])
    last_out = sqlController.GetLastSignOutTime(info[0])
    print(f"{last_in}与{last_out}直接的时间差为{last_in - last_out}")
