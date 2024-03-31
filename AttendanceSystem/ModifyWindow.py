import tkinter as tk
from tkinter import ttk

from AttendanceSystem.Employee import CheckName, CheckPosition, CheckSalary, CheckAge, CheckGender
from SqlController import sqlController
from FaceRecognition.Recognition import recognition


class ModifyWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("修改界面")

        # 划分左右两个Frame
        self.leftFrame = ttk.Frame(self)
        self.leftFrame.grid(row=0, column=0, padx=10, pady=10)

        self.rightFrame = ttk.Frame(self)
        self.rightFrame.grid(row=0, column=1, padx=10, pady=10)

        # 创建一个标签作为标题
        self.titleLabel = ttk.Label(self.leftFrame, text="修改界面\n", font=("", 20), foreground="blue")
        self.titleLabel.grid(row=0, column=0, columnspan=2)

        # 创建一个标签作为提示语
        self.tooltipLabel = ttk.Label(self.leftFrame, text="选择查询条件\n", font=("", 10))
        self.tooltipLabel.grid(row=1, column=0, sticky='w')

        # 创建两个复选框
        self.nameVar = tk.IntVar()
        self.idVar = tk.IntVar()

        # 默认选中姓名
        self.nameVar.set(1)

        # 复选框字体大小
        style = ttk.Style()
        style.configure("TCheckbutton", font=("", 12), width=5)

        self.nameCheck = ttk.Checkbutton(self.leftFrame, text="姓名", variable=self.nameVar, onvalue=1, offvalue=0,
                                         style="TCheckbutton", command=self.nameSelectCmd)
        self.nameCheck.grid(row=2, column=0, sticky='w')

        # 创建一个空白标签, 用于美观
        self.spaceLabel = ttk.Label(self.leftFrame, text=" ")
        self.spaceLabel.grid(row=3, column=0)

        self.idCheck = ttk.Checkbutton(self.leftFrame, text="编号", variable=self.idVar, onvalue=1, offvalue=0,
                                       style="TCheckbutton", command=self.idSelectCmd)
        self.idCheck.grid(row=4, column=0, sticky='w')

        # 创建输入框
        self.inputBox = ttk.Entry(self.leftFrame, width=20)
        self.inputBox.grid(row=2, column=1, rowspan=1)

        # 创建确认按钮
        self.confirmButton = ttk.Button(self.leftFrame, text="查询要编辑的人员信息", command=self.searchButtonClick,
                                        width=20)
        self.confirmButton.grid(row=4, column=1)

        # 创建一个提示标签
        self.spaceLabel = tk.Label(self.leftFrame,
                                   text="\n\n\n\n要修改的人员信息将显示如下\n(你可以直接编辑除编号外的信息)\n",
                                   font=("", 10))
        self.spaceLabel.grid(row=5, column=0)

        # 提示标签右侧设置一个Button, 用于确认修改人员信息
        self.confirmModifyButton = tk.Button(self.leftFrame, text="确认修改", command=self.confirmModifyButtonClick,
                                             width=10, height=1, background="yellow")
        self.confirmModifyButton.grid(row=5, column=1, rowspan=2)
        # 默认设置为不可用(当查询到要修改的人员信息时，设置为可用)
        self.confirmModifyButton["state"] = "disabled"

        # 创建6个标签，用于显示要删除的人员信息
        self.idLabel = ttk.Label(self.leftFrame, text="编号", font=("Arial", 10))
        self.idLabel.grid(row=6, column=0)

        self.nameLabel = ttk.Label(self.leftFrame, text="姓名", font=("Arial", 10))
        self.nameLabel.grid(row=6, column=1)

        self.positionLabel = ttk.Label(self.leftFrame, text="职位", font=("Arial", 10))
        self.positionLabel.grid(row=8, column=0)

        self.salaryLabel = ttk.Label(self.leftFrame, text="薪资", font=("Arial", 10))
        self.salaryLabel.grid(row=8, column=1)

        self.ageLabel = ttk.Label(self.leftFrame, text="年龄", font=("Arial", 10))
        self.ageLabel.grid(row=10, column=0)

        self.genderLabel = ttk.Label(self.leftFrame, text="性别", font=("Arial", 10))
        self.genderLabel.grid(row=10, column=1)

        # 创建用于显示要删除的人员信息结果的Entry
        self.idEntry = ttk.Entry(self.leftFrame, width=15)
        self.idEntry.grid(row=7, column=0)

        self.nameEntry = ttk.Entry(self.leftFrame, width=15)
        self.nameEntry.grid(row=7, column=1)

        self.positionEntry = ttk.Entry(self.leftFrame, width=15)
        self.positionEntry.grid(row=9, column=0)

        self.salaryEntry = ttk.Entry(self.leftFrame, width=15)
        self.salaryEntry.grid(row=9, column=1)

        self.ageEntry = ttk.Entry(self.leftFrame, width=15)
        self.ageEntry.grid(row=11, column=0)

        self.genderEntry = ttk.Entry(self.leftFrame, width=15)
        self.genderEntry.grid(row=11, column=1)

        # 创建用于显示要删除的人员信息结果的文本框
        self.queryResults = tk.Text(self.rightFrame, width=60, height=30)
        self.queryResults.grid(row=0, column=0)

    def nameSelectCmd(self):
        # 根据当前勾选的复选框状态，取消另一个复选框的勾选状态
        if self.nameVar.get() == 1:
            self.idVar.set(0)

    def idSelectCmd(self):
        if self.idVar.get() == 1:
            self.nameVar.set(0)

    def searchButtonClick(self):
        # 获取输入框的内容, 清空查询结果文本框
        inputText = self.inputBox.get()
        self.queryResults.delete(1.0, tk.END)

        # 根据复选框的状态，执行相应的操作
        if self.nameVar.get() == 1:
            # Name被勾选
            if inputText.isspace() or inputText == '':
                self.queryResults.insert(tk.END, "查询失败,姓名不能为空\n")
                self.confirmModifyButton["state"] = "disabled"
                return

            baseInfo = sqlController.SelectEmployeeBaseInfoByName(inputText)
            if baseInfo is None:
                self.clear()
                self.queryResults.insert(tk.END, f"未找到姓名为{inputText}的员工\n")
                self.confirmModifyButton["state"] = "disabled"
                return
            else:
                self.showBaseInfo(baseInfo[0], baseInfo[1], baseInfo[2], baseInfo[3], baseInfo[4], baseInfo[5])
                self.queryResults.insert(tk.END, f"查询姓名: {inputText}\n")
                # 查询考勤记录
                attendanceRecord = sqlController.SelectAttendanceRecordById(baseInfo[0])
                self.showAttendanceRecord(attendanceRecord)
                # 设置确认修改按钮为可用
                self.confirmModifyButton["state"] = "normal"

        elif self.idVar.get() == 1:
            # ID被勾选
            if not inputText.isdigit():
                self.queryResults.insert(tk.END, "查询失败, 编号需要为数字\n")
                self.confirmModifyButton["state"] = "disabled"
                return

            baseInfo = sqlController.SelectEmployeeBaseInfoById(inputText)
            if baseInfo is None:
                self.clear()
                self.queryResults.insert(tk.END, f"未找到编号为{inputText}的员工\n")
                self.confirmModifyButton["state"] = "disabled"
                return
            else:
                self.showBaseInfo(baseInfo[0], baseInfo[1], baseInfo[2], baseInfo[3], baseInfo[4], baseInfo[5])
                self.queryResults.insert(tk.END, f"查询编号: {inputText}\n")
                # 查询考勤记录
                attendanceRecord = sqlController.SelectAttendanceRecordById(baseInfo[0])
                self.showAttendanceRecord(attendanceRecord)
                # 设置确认修改按钮为可用
                self.confirmModifyButton["state"] = "normal"

    def confirmModifyButtonClick(self):
        print("确认修改")

        id = self.idEntry.get()
        name = self.nameEntry.get()
        position = self.positionEntry.get()
        salary = self.salaryEntry.get().replace('元/月', '')
        age = self.ageEntry.get().replace('岁', '')
        gender = self.genderEntry.get()
        if not self.checkInfo(name, position, salary, age, gender):  # 有不合法的输入
            return
        # 更新数据库信息
        sqlController.UpdateEmployeeBaseInfo(id, name, position, salary, age, 0 if gender == "男" else 1)
        self.queryResults.delete(1.0, tk.END)
        self.queryResults.insert(tk.END, f"编号为{id}的员工信息已修改\n")
        self.confirmModifyButton["state"] = "disabled"
        # 更新当前程序中人脸识别所用的数据库信息
        recognition.updateKnownFeatureList()


    def showBaseInfo(self, _id, _name, _position, _salary, _age, _gender):
        # 显示基本信息
        self.idEntry["state"] = "normal"  # 设置为可写, 用于显示编号
        self.idEntry.delete(0, tk.END)
        self.idEntry.insert(0, _id)
        self.idEntry["state"] = "readonly"  # 设置为只读, 避免用户修改编号

        self.nameEntry.delete(0, tk.END)
        self.nameEntry.insert(0, _name)

        self.positionEntry.delete(0, tk.END)
        self.positionEntry.insert(0, _position)

        self.salaryEntry.delete(0, tk.END)
        self.salaryEntry.insert(0, f"{_salary}元/月")

        self.ageEntry.delete(0, tk.END)
        self.ageEntry.insert(0, f"{_age}岁")

        self.genderEntry.delete(0, tk.END)
        self.genderEntry.insert(0, "男" if int(_gender) == 0 else "女")

    def showAttendanceRecord(self, _record):
        # 显示考勤记录
        # _record是一个列表，每个元素是一个AttendanceRecord对象, 用于显示签到时间和签到状态
        self.queryResults.insert(tk.END, "考勤记录如下: \n")
        # 对列表按照时间排序
        _record.sort(key=lambda x: x.datetime)
        # AttendanceRecord对象被划分为4列显示, 分别为日期, 上下午(am/pm), 当日具体时间, 签到状态(签到/签退)
        # 第一行显示列名
        self.queryResults.insert(tk.END, "日期\t\tam/pm\t\t时间\t\t签到状态\n")
        for record in _record:
            date, time = record.datetime.date(), record.datetime.time()
            ampm = '上午' if int(time.hour) < 12 else '下午'
            status = '签到' if record.status == 0 else '签退'
            self.queryResults.insert(tk.END, f"{date}\t\t{ampm}\t\t{time}\t\t{status}\n")

    def checkInfo(self, name, position, salary, age, gender):
        tipLabelText = "以下内容不合法:(请检查后重新输入)\n"

        if not CheckName(name):
            tipLabelText += "姓名(只包含字母或中文, 长度不超过50字符)\n"
        if not CheckPosition(position):
            tipLabelText += "职位(只包含字母或中文, 长度不超过50字符)\n"
        if not CheckSalary(salary):
            tipLabelText += "薪资(不能为负数)\n"
        if not CheckAge(age):
            tipLabelText += "年龄(介于18-65之间)\n"
        if not CheckGender(gender):
            tipLabelText += "性别(选择男/女)\n"

        if tipLabelText != "以下内容不合法:(请检查后重新输入)\n":  # 有不合法的输入
            self.queryResults.delete(1.0, tk.END)
            self.queryResults.insert(tk.END, tipLabelText)
            return False

        else:
            return True

    def clear(self):
        self.idEntry["state"] = "normal"
        self.idEntry.delete(0, tk.END)
        self.nameEntry.delete(0, tk.END)
        self.positionEntry.delete(0, tk.END)
        self.salaryEntry.delete(0, tk.END)
        self.ageEntry.delete(0, tk.END)
        self.genderEntry.delete(0, tk.END)
        self.queryResults.delete(1.0, tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    queryWindow = ModifyWindow(root)
    root.mainloop()
