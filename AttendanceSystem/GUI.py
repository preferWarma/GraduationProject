import tkinter as tk
from datetime import datetime
from tkinter import ttk, Entry, Label, StringVar

import cv2
from PIL import Image, ImageTk

from AttendanceSystem.Manager import manager
from FaceRecognition.Recognition import recognition
from SqlController import sqlController


class AdminGui:
    def __init__(self, master):
        self.retNameList = []  # 保存识别出的人名列表
        self.master = master
        master.title("管理员界面")

        # 左侧按钮容器
        self.left_frame = tk.Frame(master, padx=20, pady=20)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # 在顶部居中显示Label
        label = tk.Label(master, text="XXX考勤系统界面", font=("Helvetica", 20))
        label.pack(side=tk.TOP, pady=10)

        # 创建按钮样式
        self.style = ttk.Style()
        # 设置按钮样式，包括宽度和高度
        self.style.configure("TButton", padding=(10, 5, 10, 5), width=30, height=15)

        # 左侧按钮
        self.btnAdd = ttk.Button(self.left_frame, text="新增人员", command=self.addPerson, style="TButton")
        self.btnView = ttk.Button(self.left_frame, text="查看人员信息", command=self.queryPerson, style="TButton")
        self.btnEdit = ttk.Button(self.left_frame, text="修改人员信息", command=self.modifyPerson, style="TButton")
        self.btnDelete = ttk.Button(self.left_frame, text="删除人员", command=self.deletePerson, style="TButton")

        self.btnAdd.grid(row=0, column=0, pady=10)
        self.btnView.grid(row=1, column=0, pady=10)
        self.btnEdit.grid(row=2, column=0, pady=10)
        self.btnDelete.grid(row=3, column=0, pady=10)

        # 登录界面
        self.loginNameLabel = ttk.Label(self.left_frame, text="用户名:")
        self.loginNameEntry = ttk.Entry(self.left_frame)
        self.loginNameLabel.grid(row=4, column=0, padx=10, pady=10)
        self.loginNameEntry.grid(row=4, column=1, padx=10, pady=10)
        self.loginPasswordLabel = Label(self.left_frame, text="密码:")
        self.loginPasswordEntry = Entry(self.left_frame)
        self.loginPasswordLabel.grid(row=5, column=0, padx=10, pady=10)
        self.loginPasswordEntry.grid(row=5, column=1, padx=10, pady=10)
        self.loginButton = ttk.Button(self.left_frame, text="登录", command=self.login, style="TButton")
        self.loginButton.grid(row=6, column=0, pady=10)

        # 签到界面
        self.signInButton = tk.Button(self.left_frame, text="签到", command=self.signIn, width=10, height=1)
        self.signInButton.grid(row=10, column=0, padx=10, pady=10, sticky=tk.W)
        self.signOutButton = tk.Button(self.left_frame, text="签退", command=self.signOut, width=10, height=1)
        self.signOutButton.grid(row=10, column=1, padx=10, pady=10)

        # 右侧摄像头输入流显示框
        self.videoLabel = ttk.Label(master)
        self.videoLabel.pack(side=tk.RIGHT, padx=10)

        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        self.showVideo()

        # 默认显示登录界面
        self.showLoginSection()

        # 登录失败提示
        self.loginFailLabel = ttk.Label(self.left_frame, text="", foreground='red',
                                        font=("Helvetica", 15))
        self.loginFailLabel.grid(row=6, column=0, pady=10, columnspan=2)

        # 签到提示
        self.signTooltipLabel = ttk.Label(self.left_frame, text="", foreground='red',
                                          font=("Helvetica", 15))
        self.signTooltipLabel.grid(row=12, column=0, pady=10, columnspan=2)

    def showVideo(self):
        self.retNameList = []
        _, frame = self.cap.read()
        frame, self.retNameList = recognition.handle(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.videoLabel.imgtk = imgtk
        self.videoLabel.configure(image=imgtk)
        self.videoLabel.after(10, self.showVideo)  # 10ms后调用showVideo

    def showManagerSection(self):
        # 隐藏登录界面
        self.loginNameLabel.grid_forget()
        self.loginNameEntry.grid_forget()
        self.loginPasswordLabel.grid_forget()
        self.loginPasswordEntry.grid_forget()
        self.loginButton.grid_forget()
        # 显示管理员界面
        self.btnAdd.grid(row=0, column=0, pady=10)
        self.btnView.grid(row=1, column=0, pady=10)
        self.btnEdit.grid(row=2, column=0, pady=10)
        self.btnDelete.grid(row=3, column=0, pady=10)

    def showLoginSection(self):
        # 隐藏管理员界面
        self.btnAdd.grid_forget()
        self.btnView.grid_forget()
        self.btnEdit.grid_forget()
        self.btnDelete.grid_forget()
        # 显示登录界面
        self.loginNameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.loginNameEntry.grid(row=0, column=1, padx=10, pady=10)
        self.loginPasswordLabel.grid(row=1, column=0, padx=1, pady=10)
        self.loginPasswordEntry.grid(row=1, column=1, padx=1, pady=10)
        self.loginButton.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        # 实现登录逻辑
        if self.loginNameEntry.get().isspace() or self.loginPasswordEntry.get().isspace() \
                or self.loginNameEntry.get() == '' or self.loginPasswordEntry.get() == '':
            self.loginFailLabel.configure(text="用户名或密码不能为空", foreground='red')
            return
        if manager.Login(self.loginNameEntry.get(), self.loginPasswordEntry.get()):
            self.showManagerSection()
            self.loginFailLabel.configure(text="")
        else:
            self.loginFailLabel.configure(text="用户名或密码错误", foreground='red')

    def signIn(self):
        if len(self.retNameList) == 0:
            self.signTooltipLabel.configure(text="没有检测到人脸", foreground='red')
            return
        for name in self.retNameList:
            person = manager.GetPersonByName(name)
            if person is not None:
                if person.SignIn():
                    manager.UpdatePerson(person.id, person.name, person.record)
                    self.signTooltipLabel.configure(text="签到成功", foreground='green')
                else:
                    self.signTooltipLabel.configure(text="半小时内只能签到一次", foreground='red')

    def signOut(self):
        if len(self.retNameList) == 0:
            self.signTooltipLabel.configure(text="没有检测到人脸", foreground='red')
            return
        for name in self.retNameList:
            person = manager.GetPersonByName(name)
            if person is not None:
                if person.SignOut():
                    manager.UpdatePerson(person.id, person.name, person.record)
                    self.signTooltipLabel.configure(text="签退成功", foreground='green')
                else:
                    self.signTooltipLabel.configure(text="半小时内只能签退一次", foreground='red')

    def addPerson(self):
        # 实现新增人员的逻辑
        AddPersonWindow(self.master, self)

    def queryPerson(self):
        # 实现查看人员信息的逻辑
        QueryPersonWindow(self.master, self)

    def modifyPerson(self):
        # 实现修改人员信息的逻辑
        ModifyPersonWindow(self.master, self)

    def deletePerson(self):
        # 实现删除人员的逻辑
        DeletePersonWindow(self.master, self)


class AddPersonWindow(tk.Toplevel):
    def __init__(self, master, adminGui):
        tk.Toplevel.__init__(self, master)
        self.title("新增人员窗口")
        self.adminGui = adminGui  # 保存AdminGUI实例

        # 创建第1行的Label和Entry
        self.labelName = Label(self, text="姓名:")
        self.entryName = Entry(self)
        self.labelName.grid(row=1, column=0, padx=10, pady=10)
        self.entryName.grid(row=1, column=1, padx=10, pady=10)

        # 创建录入人脸按钮
        self.faceButton = ttk.Button(self, text="录入人脸", command=self.recordFace, style="TButton")
        self.faceButton.grid(row=2, column=0, columnspan=2, pady=10)

        # 成员变量保存Id和姓名
        self.personId = None
        self.personName = None

    def recordFace(self):
        # 获取输入的Id和姓名
        self.personName = self.entryName.get()
        if self.personName.isspace() or self.personName == '未命名':
            self.entryName.insert(0, "未命名")
            return
        # 实现录入人脸的逻辑，可以使用self.personId和self.personName和self.adminGui.cap
        manager.AddPerson(self.personName, self.adminGui.cap)
        (Label(self, text="录入成功", foreground='green', font=("Helvetica", 15))
         .grid(row=3, column=0, columnspan=2, pady=10))


class DeletePersonWindow(tk.Toplevel):
    def __init__(self, master, adminGui):
        tk.Toplevel.__init__(self, master)
        self.title("删除人员窗口")
        self.adminGui = adminGui  # 保存AdminGUI实例

        # 创建Label和Entry
        self.labelId = Label(self, text="要删除的人员Id:")
        self.entryId = Entry(self)
        self.labelId.grid(row=0, column=0, padx=10, pady=10)
        self.entryId.grid(row=0, column=1, padx=10, pady=10)

        # 创建删除人员按钮
        self.deleteButton = tk.Button(self, text="删除人员", command=self.deletePerson)
        self.deleteButton.grid(row=1, column=0, columnspan=2, pady=10)

        # 成员变量保存要删除的人员Id
        self.personIdToDelete = None
        self.toolTip = Label(self, text="请输入要删除的人员Id", font=("Helvetica", 15))

    def deletePerson(self):
        # 获取输入的要删除的人员Id
        self.personIdToDelete = int(self.entryId.get())
        if not self.checkIdExist():
            self.toolTip.configure(text="Id不存在", foreground='red')
            self.toolTip.grid(row=2, column=0, columnspan=2, pady=10)
            return
        # 实现删除人员的逻辑
        manager.DeletePerson(self.personIdToDelete)
        self.toolTip.configure(text="删除成功", foreground='green')
        self.toolTip.grid(row=2, column=0, columnspan=2, pady=10)

    def checkIdExist(self) -> bool:
        # 检查输入的Id是否存在
        return sqlController.SelectPersonById(self.personIdToDelete) is not None


class QueryPersonWindow(tk.Toplevel):
    def __init__(self, master, adminGui):
        tk.Toplevel.__init__(self, master)
        self.title("查询人员窗口")
        self.adminGui = adminGui  # 保存AdminGUI实例

        # 创建ID输入栏
        self.labelId = ttk.Label(self, text="请输入人员Id:")
        self.entryId = ttk.Entry(self)
        self.labelId.grid(row=0, column=0, padx=10, pady=10)
        self.entryId.grid(row=0, column=1, padx=10, pady=10)

        # 创建查询按钮
        self.queryButton = ttk.Button(self, text="查询", command=self.queryPerson)
        self.queryButton.grid(row=1, column=0, columnspan=2, pady=10)

        # 创建显示查询结果的Label
        self.resultLabel = ttk.Label(self, text="查询结果将在这里显示", font=("Helvetica", 15), anchor='w')
        self.resultLabel.grid(column=0, columnspan=2, pady=10)

        # 成员变量保存要查询的人员Id
        self.personIdToQuery = None

    def queryPerson(self):
        # 获取输入的要查询的人员Id
        if not self.entryId.get().isdigit():
            self.resultLabel.configure(text="请输入正确的ID格式", foreground='red')
            return
        self.personIdToQuery = int(self.entryId.get())
        # 实现查询人员的逻辑
        person = manager.GetPersonById(self.personIdToQuery)
        # 根据实际情况更新self.resultLabel的文本
        if person is None:
            self.resultLabel.configure(text="Id不存在", foreground='red')
            return
        self.resultLabel.configure(text=f"姓名: {person.name}\n签到记录: \n{person.recordToString()}",
                                   foreground='black')


class ModifyPersonWindow(tk.Toplevel):
    def __init__(self, master, adminGui):
        tk.Toplevel.__init__(self, master)
        self.title("修改人员窗口")
        self.adminGui = adminGui  # 保存AdminGUI实例

        # 创建ID输入栏
        self.labelId = Label(self, text="请输入人员Id:")
        self.entryId = Entry(self)
        self.labelId.grid(row=0, column=0, padx=10, pady=10)
        self.entryId.grid(row=0, column=1, padx=10, pady=10)

        # 创建选择修改的Radiobutton
        self.modifyOption = StringVar()
        self.modifyOption.set("Name")  # 默认选项是修改姓名
        self.modifyNameButton = ttk.Radiobutton(self, text="修改姓名", variable=self.modifyOption, value="Name",
                                                command=self.showNameSection)
        self.modifyRecordButton = ttk.Radiobutton(self, text="修改记录", variable=self.modifyOption, value="Record",
                                                  command=self.showRecordSection)
        self.modifyNameButton.grid(row=1, column=0, columnspan=2, pady=5)
        self.modifyRecordButton.grid(row=2, column=0, columnspan=2, pady=5)

        # 创建姓名修改部分
        self.newNameLabel = Label(self, text="新的姓名:")
        self.newNameEntry = Entry(self)
        self.newNameLabel.grid(row=3, column=0, padx=10, pady=5)
        self.newNameEntry.grid(row=3, column=1, padx=10, pady=5)

        # 创建记录修改部分
        self.dateLabel = Label(self, text="日期:")
        self.timeLabel = Label(self, text="时间:")
        self.dateEntry = Entry(self)
        self.timeEntry = Entry(self)
        self.dateLabel.grid(row=4, column=0, padx=10, pady=5)
        self.dateEntry.grid(row=4, column=1, padx=10, pady=5)
        self.timeLabel.grid(row=5, column=0, padx=10, pady=5)
        self.timeEntry.grid(row=5, column=1, padx=10, pady=5)

        # 创建签到和签退按钮
        self.signInButton = ttk.Button(self, text="签到", command=self.signIn)
        self.signOutButton = ttk.Button(self, text="签退", command=self.signOut)
        self.signInButton.grid(row=6, column=0, pady=5)
        self.signOutButton.grid(row=6, column=1, pady=5)

        # 创建修改按钮
        self.modifyButton = ttk.Button(self, text="修改", command=self.modifyPersonName)
        self.modifyButton.grid(row=7, column=0, columnspan=2, pady=10)

        # 创建显示修改结果的Label
        self.resultLabel = Label(self, text="修改结果将在这里显示")
        self.resultLabel.grid(row=8, column=0, columnspan=2, pady=10)

        # 成员变量保存要修改的人员Id和修改选项
        self.personIdToModify = None
        self.personToModify = None

        self.showNameSection()  # 默认显示姓名修改部分

    def showNameSection(self):
        # 隐藏记录修改部分
        self.dateLabel.grid_forget()
        self.dateEntry.grid_forget()
        self.timeLabel.grid_forget()
        self.timeEntry.grid_forget()
        self.signInButton.grid_forget()
        self.signOutButton.grid_forget()

        # 显示姓名修改部分
        self.newNameLabel.grid(row=3, column=0, padx=10, pady=5)
        self.newNameEntry.grid(row=3, column=1, padx=10, pady=5)
        self.modifyButton.grid(row=7, column=0, columnspan=2, pady=10)

    def showRecordSection(self):
        # 隐藏姓名修改部分
        self.newNameLabel.grid_forget()
        self.newNameEntry.grid_forget()
        self.modifyButton.grid_forget()

        # 显示记录修改部分
        self.dateLabel.grid(row=4, column=0, padx=10, pady=5)
        self.dateEntry.grid(row=4, column=1, padx=10, pady=5)
        self.timeLabel.grid(row=5, column=0, padx=10, pady=5)
        self.timeEntry.grid(row=5, column=1, padx=10, pady=5)
        self.signInButton.grid(row=6, column=0, pady=5)
        self.signOutButton.grid(row=6, column=1, pady=5)

        # 默认显示当前日期和时间
        self.dateEntry.delete(0, tk.END)
        self.dateEntry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.timeEntry.delete(0, tk.END)
        self.timeEntry.insert(0, datetime.now().strftime('%H:%M:%S'))

    def checkPersonExist(self) -> bool:
        # 获取输入的要修改的人员Id和修改选项
        self.personIdToModify = self.entryId.get()

        if not self.personIdToModify.isdigit():
            self.resultLabel.configure(text="请输入正确的ID格式", foreground='red')
            return False
        self.personIdToModify = int(self.personIdToModify)
        self.personToModify = manager.GetPersonById(self.personIdToModify)
        # 根据实际情况更新self.resultLabel的文本
        if self.personToModify is None:
            self.resultLabel.configure(text="Id不存在", foreground='red')
            return False
        return True

    def modifyPersonName(self):
        if not self.checkPersonExist():
            return
        if self.modifyOption.get() == "Name":
            self.modifyName()

    def modifyName(self):
        # 获取输入的新的姓名
        newName = self.newNameEntry.get()
        if newName.isspace() or newName == '未命名':
            self.newNameEntry.insert(0, "未命名")
            return
        manager.UpdatePerson(self.personIdToModify, newName, self.personToModify.record)
        self.resultLabel.configure(text="姓名修改成功", foreground='green')

    def checkDateTimeFormat(self) -> bool:
        # 获取输入的日期和时间
        date = self.dateEntry.get()
        time = self.timeEntry.get()
        # 检查日期格式是否正确(yyyy-mm-dd), 时间格式是否正确(HH:MM:SS)
        try:
            datetime.strptime(date, '%Y-%m-%d')
            datetime.strptime(time, '%H:%M:%S')
            return True
        except ValueError:
            self.resultLabel.configure(text="日期或时间格式不正确, 请日期格式为yyyy-mm-dd, 时间格式为HH:MM:SS",
                                       foreground='red', font=("Helvetica", 15))
            return False

    def signIn(self):
        # 实现签到逻辑
        if self.checkDateTimeFormat():
            if self.checkPersonExist():
                self.personToModify.SignInWithTime(self.dateEntry.get(), self.timeEntry.get())
                manager.UpdatePerson(self.personIdToModify, self.personToModify.name, self.personToModify.record)
                self.resultLabel.configure(text="签到成功", foreground='green')

    def signOut(self):
        # 实现签退逻辑
        if self.checkDateTimeFormat():
            if self.checkPersonExist():
                self.personToModify.SignOutWithTime(self.dateEntry.get(), self.timeEntry.get())
                manager.UpdatePerson(self.personIdToModify, self.personToModify.name, self.personToModify.record)
                self.resultLabel.configure(text="签退成功", foreground='green')


if __name__ == '__main__':
    root = tk.Tk()
    app = AdminGui(root)
    root.geometry("1000x600")
    root.mainloop()
