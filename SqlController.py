import datetime

import mysql.connector
import numpy as np

from AttendanceSystem.Employee import AttendanceRecord


class SqlController:
    def __init__(self, host="localhost", user="root", passwd="Aa112211", database="graduation"):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )  # 连接数据库
        self.cursor = self.db.cursor()  # 创建游标

    # TODO: 需要重构
    def UpdatePerson(self, id: int, name, record: dict) -> None:
        sql = "update PersonDataBase set record = %s, name = %s where id = %s"
        val = (str(record), name, id)
        self.cursor.execute(sql, val)
        self.db.commit()

    # TODO: 重构到此

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

    def SelectAttendanceRecordById(self, EmployeeID):
        sql = "select * from attendance where EmployeeID = %s"
        self.cursor.execute(sql, (EmployeeID,))
        sqlResult = self.cursor.fetchall()
        # 将查询结果转换为AttendanceRecord对象(签到时间, 签到状态)
        ret = []
        for result in sqlResult:
            ret.append(AttendanceRecord(result[2], result[3]))
        return ret

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

    def Login(self, userId: str, password: str) -> bool:
        sql = "select * from managerDataBase where id = %s and password = %s"
        self.cursor.execute(sql, (userId, password))
        result = self.cursor.fetchone()
        return result is not None

    def ExecuteWithSql(self, sql: str):
        self.cursor.execute(sql)
        self.db.commit()

    def SelectWithSql(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def __del__(self):
        self.db.close()


sqlController = SqlController()

if __name__ == '__main__':
    info = sqlController.SelectEmployeeBaseInfoByName("lyf")
    print(info)
    # now_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # sqlController.InsertAttendanceRecord(info[0], now_datetime, 1)
    sqlController.UpdateEmployeeBaseInfo(info[0], "cjy", "student", 10000, 20, 1)
    print(sqlController.SelectEmployeeBaseInfoByName("cjy"))

    pass
