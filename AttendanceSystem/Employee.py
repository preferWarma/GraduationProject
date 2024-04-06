class AttendanceRecord:
    def __init__(self, recordId, employeeId, datetime, type):
        self.recordID = recordId  # 记录编号
        self.employeeID = employeeId  # 员工编号
        self.datetime = datetime  # 签到时间
        self.type = type  # 签到状态(0: 签到/1: 签退)

    def __str__(self):
        return str(self.datetime) + ' ' + ('签到' if self.type == 0 else '签退')


class User:
    def __init__(self, userId, password, userType):
        self.userId = userId
        self.password = password
        self.userType = userType


def CheckName(name: str) -> bool:
    """
    检查姓名是否包含字母、空格或者中文字符，并且姓名长度不超过50个字符
    :param name: 姓名
    :return: True: 合法/False: 不合法
    """
    # 检查姓名是否为空
    if not name or name.isspace() or name == '':
        return False

    # 检查姓名是否只包含字母或中文字符
    if not all(char.isalpha() or '\u4e00' <= char <= '\u9fff' for char in name):
        return False

    # 检查姓名长度是否超过50个字符
    if len(name) > 50:
        return False

    return True


def CheckPosition(position: str) -> bool:
    """
    检查职位是否包含字母、空格或者中文字符，并且职位长度不超过50个字符
    :param position: 职位
    :return: True: 合法/False: 不合法
    """
    # 检查职位是否为空
    if not position or position.isspace() or position == '':
        return False

    # 检查职位是否只包含字母或中文字符
    if not all(char.isalpha() or '\u4e00' <= char <= '\u9fff' for char in position):
        return False

    # 检查职位长度是否超过50个字符
    if len(position) > 50:
        return False

    return True


def CheckSalary(salary: str) -> bool:
    """
    检查薪资是否为正整数
    :param salary: 薪资
    :return: True: 合法/False: 不合法
    """
    # 去掉薪资中的"元/月"
    salary = salary.replace('元/月', '')

    # 检查薪资是否为空
    if not salary or salary.isspace() or salary == '':
        return False

    # 检查薪资是否为正整数
    if not salary.isdigit() or int(salary) <= 0:
        return False

    return True


def CheckAge(age: str) -> bool:
    """
    检查年龄是否为正整数
    :param age: 年龄
    :return: True: 合法/False: 不合法
    """
    # 去掉年龄中的"岁"
    age = age.replace('岁', '')

    # 检查年龄是否为空
    if not age or age.isspace() or age == '':
        return False

    # 检查年龄是否为正整数
    if not age.isdigit() or int(age) <= 18 or int(age) > 65:
        return False

    return True


def CheckGender(gender: str) -> bool:
    return gender == '男' or gender == '女'


def CheckPermission(permission: str) -> bool:
    return permission == '普通员工' or permission == '管理员'


if __name__ == '__main__':
    # record = AttendanceRecord(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0)
    # print(record)
    # record = AttendanceRecord(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1)
    # print(record)
    # record = AttendanceRecord(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0)
    # print(record)
    # record = AttendanceRecord(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1)
    # print(record)
    print(CheckName("张三"))
    print(CheckName("zhangsan"))
    print(CheckName("张三san"))
    print(CheckName("123"))
    print(CheckName(" "))
    print(CheckName(""))
