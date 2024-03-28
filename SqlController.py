import mysql.connector
import numpy as np


class SqlController:
    def __init__(self, host="localhost", user="root", passwd="Aa112211", database="graduation"):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )  # 连接数据库
        self.cursor = self.db.cursor()  # 创建游标

    def Insert(self, name: str, feature: np.array) -> None:
        """
        插入数据
        :param name: 姓名
        :param feature: 特征
        """
        sql = "insert into KnownFeatureDataBase (name, feature) values (%s, %s)"
        val = (name, str(list(feature)))
        self.cursor.execute(sql, val)
        self.db.commit()

    def InsertPerson(self, id: int, name: str, record: dict) -> None:
        sql = "insert into PersonDataBase (id, name, record) values (%s, %s, %s)"
        val = (id, name, str(record))
        self.cursor.execute(sql, val)
        self.db.commit()

    def Update(self, name: str, feature: np.array) -> None:
        """
        更新数据
        :param name: 姓名
        :param feature: 特征
        """
        sql = "update KnownFeatureDataBase set feature = %s where name = %s"
        val = (str(list(feature)), name)
        self.cursor.execute(sql, val)
        self.db.commit()

    def UpdatePerson(self, id: int, name, record: dict) -> None:
        sql = "update PersonDataBase set record = %s, name = %s where id = %s"
        val = (str(record), name, id)
        self.cursor.execute(sql, val)
        self.db.commit()

    def InsertWithJudgeExist(self, name: str, feature: np.array) -> None:
        """
        插入数据, 判断是否存在
        :param name: 姓名
        :param feature: 特征
        """
        # 查询是否存在
        sql = "select * from KnownFeatureDataBase where name = %s"
        self.cursor.execute(sql, (name,))
        result = self.cursor.fetchone()
        if result is None:
            self.Insert(name, feature)
        else:
            self.Update(name, feature)

    def InsertPersonWithJudgeExist(self, id: int, name: str, record: dict) -> None:
        sql = "select * from PersonDataBase where id = %s"
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        if result is None:
            self.InsertPerson(id, name, record)
        else:
            self.UpdatePerson(id, name, record)

    def Select(self, name: str) -> np.array:
        """
        查询数据
        :param name: 姓名
        :return: 特征
        """
        sql = "select feature from KnownFeatureDataBase where name = %s"
        self.cursor.execute(sql, (name,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return np.fromstring(result[0][1:-1], sep=', ')

    def SelectPersonById(self, id: int):
        sql = "select name, record from PersonDataBase where id = %s"
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return result[0], eval(result[1])

    def SelectPersonByName(self, name: str):
        sql = "select id, record from PersonDataBase where name = %s"
        self.cursor.execute(sql, (name,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return result[0], eval(result[1])

    def SelectAll(self) -> list:
        """
        查询所有数据
        :return: 所有数据
        """
        sql = "select * from KnownFeatureDataBase"
        self.cursor.execute(sql)
        selectResult = self.cursor.fetchall()
        ret = []
        for result in selectResult:
            ret.append([result[0], np.fromstring(result[1][1:-1], sep=', ')])
        return ret

    def Delete(self, name: str) -> None:
        """
        删除数据
        :param name: 姓名
        """
        sql = "delete from KnownFeatureDataBase where name = %s"
        self.cursor.execute(sql, (name,))
        self.db.commit()

    def DeletePerson(self, id: int) -> None:
        sql = "delete from PersonDataBase where id = %s"
        self.cursor.execute(sql, (id,))
        self.db.commit()

    def GetNewId(self) -> int:
        sql = "select max(id) from PersonDataBase"
        self.cursor.execute(sql)
        selectResult = self.cursor.fetchone()
        if selectResult[0] is None:
            return 1
        return selectResult[0] + 1

    def Login(self, userId: str, password: str) -> bool:
        sql = "select * from managerDataBase where id = %s and password = %s"
        self.cursor.execute(sql, (userId, password))
        result = self.cursor.fetchone()
        return result is not None

    def __del__(self):
        self.db.close()


sqlController = SqlController()

if __name__ == '__main__':
    # sqlController.Insert("test", np.array([1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    # feature = sqlController.Select("test")
    # print(feature)
    # features = sqlController.SelectAll()
    a = sqlController.SelectPersonById(2)
    print(a)
    pass
