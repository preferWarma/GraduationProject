import tkinter as tk
from datetime import datetime
from tkinter import ttk, Entry, Label, StringVar

import cv2
from PIL import Image, ImageTk

from AttendanceSystem.DeleteWindow import DeleteWindow
from AttendanceSystem.InsertWindow import InsertWindow
from AttendanceSystem.QueryWindow import QueryWindow
from FaceRecognition.Recognition import recognition
from SqlController import sqlController


class MainGUI:
    def __init__(self, master):
        self.retInfoList = []  # 保存识别出的人员信息列表[[id, name], ...]
        self.master = master
        master.title("管理员界面")

        # 在顶部居中显示Label
        self.title = ttk.Label(master, text="人脸识别考勤系统界面", font=("Arial", 35), background='white',
                               foreground='orange')
        self.title.pack(side=tk.TOP, pady=10)

        # 左上角显示当前时间
        self.timeLabel = ttk.Label(master, text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), font=("Helvetica", 15))
        self.timeLabel.pack(side=tk.TOP, pady=10)

        # 左侧按钮容器
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # 右侧摄像头输入流显示框
        self.videoLabel = ttk.Label(master)
        self.videoLabel.pack(side=tk.RIGHT, padx=10)

        # 创建按钮样式
        self.style = ttk.Style()
        # 设置按钮样式，包括宽度和高度
        self.style.configure("TButton", padding=(10, 5, 10, 5), width=35, height=15)

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
        self.loginNameLabel = ttk.Label(self.left_frame, text="用户名: ", font=("Helvetica", 15), justify=tk.LEFT)
        self.loginNameEntry = ttk.Entry(self.left_frame, width=20)
        self.loginNameLabel.grid(row=4, column=0, padx=10, pady=10)
        self.loginNameEntry.grid(row=4, column=1, padx=10, pady=10)

        self.loginPasswordLabel = Label(self.left_frame, text=" 密码: ", font=("Helvetica", 15), justify=tk.LEFT)
        self.loginPasswordEntry = Entry(self.left_frame, show='*', width=20)
        self.loginPasswordLabel.grid(row=5, column=0, padx=10, pady=10)
        self.loginPasswordEntry.grid(row=5, column=1, padx=10, pady=10)

        self.loginButton = ttk.Button(self.left_frame, text="登录", command=self.login, style="TButton")
        self.loginButton.grid(row=6, column=0, pady=10)

        # 签到界面
        self.signInButton = tk.Button(self.left_frame, text="签到", command=self.signIn, width=12, height=2)
        self.signInButton.grid(row=10, column=0, padx=10, pady=10, sticky=tk.W)
        self.signOutButton = tk.Button(self.left_frame, text="签退", command=self.signOut, width=12, height=2)
        self.signOutButton.grid(row=10, column=1, padx=10, pady=10, sticky=tk.E)

        # 登录失败提示
        self.loginFailLabel = ttk.Label(self.left_frame, text="", foreground='red', font=("Helvetica", 15))
        self.loginFailLabel.grid(row=6, column=0, pady=10, columnspan=2)

        # 签到提示
        self.signTooltipLabel = ttk.Label(self.left_frame, text="", foreground='red', font=("Helvetica", 15))
        self.signTooltipLabel.grid(row=12, column=0, pady=10, columnspan=2)

        # 退出登录按钮
        self.logoutButton = ttk.Button(self.left_frame, text="退出登录", command=self.showLoginSection, style="TButton")
        self.logoutButton.grid(row=13, column=0, pady=10, columnspan=2)

        # 默认显示登录界面
        self.showLoginSection()

        # 打开摄像头
        self.camera = cv2.VideoCapture(0)
        self.update()

    def update(self):
        # 更新时间
        self.timeLabel.configure(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # 更新视频流
        _, frame = self.camera.read()
        frame, self.retInfoList, _ = recognition.handle(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)  # 使用PIL进行图像格式转换, 使其在tkinter中兼容显示
        self.videoLabel.imgtk = imgtk
        self.videoLabel.configure(image=imgtk)

        # 每10ms更新一次
        self.videoLabel.after(10, self.update)

    def showManagerSection(self):
        # 隐藏登录界面
        self.loginNameLabel.grid_forget()
        self.loginNameEntry.grid_forget()
        self.loginPasswordLabel.grid_forget()
        self.loginPasswordEntry.grid_forget()
        self.loginButton.grid_forget()
        # 显示管理员界面
        self.btnAdd.grid(row=0, column=0, pady=10, columnspan=2)
        self.btnView.grid(row=1, column=0, pady=10, columnspan=2)
        self.btnEdit.grid(row=2, column=0, pady=10, columnspan=2)
        self.btnDelete.grid(row=3, column=0, pady=10, columnspan=2)
        self.logoutButton.grid(row=13, column=0, pady=10, columnspan=2)
        # 清空所有提示和输入框
        self.loginFailLabel.configure(text="")
        self.signTooltipLabel.configure(text="")
        self.loginNameEntry.delete(0, tk.END)
        self.loginPasswordEntry.delete(0, tk.END)

    def showLoginSection(self):
        # 隐藏管理员界面
        self.btnAdd.grid_forget()
        self.btnView.grid_forget()
        self.btnEdit.grid_forget()
        self.btnDelete.grid_forget()
        self.logoutButton.grid_forget()
        # 显示登录界面
        self.loginNameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.loginNameEntry.grid(row=0, column=1, padx=10, pady=10)
        self.loginPasswordLabel.grid(row=1, column=0, padx=1, pady=10)
        self.loginPasswordEntry.grid(row=1, column=1, padx=1, pady=10)
        self.loginButton.grid(row=2, column=0, columnspan=2, pady=10)
        # 清空所有提示和输入框
        self.loginFailLabel.configure(text="")
        self.signTooltipLabel.configure(text="")
        self.loginNameEntry.delete(0, tk.END)
        self.loginPasswordEntry.delete(0, tk.END)

    def login(self):
        # 实现登录逻辑
        if self.loginNameEntry.get().isspace() or self.loginPasswordEntry.get().isspace() \
                or self.loginNameEntry.get() == '' or self.loginPasswordEntry.get() == '':
            self.loginFailLabel.configure(text="用户名或密码不能为空", foreground='red')
            return
        if sqlController.Login(self.loginNameEntry.get(), self.loginPasswordEntry.get()):
            self.showManagerSection()
            self.loginFailLabel.configure(text="")
        else:
            self.loginFailLabel.configure(text="用户名或密码错误", foreground='red')

    # TODO: 需要修改
    def signIn(self):
        if len(self.retInfoList) == 0:
            self.signTooltipLabel.configure(text="没有检测到录入的人脸", foreground='red')
            return
        for info in self.retInfoList:
            info_id, info_name = info[0], info[1]
            person = sqlController.SelectEmployeeBaseInfoById(info_id)
            if person is not None:
                if person.SignIn():
                    # TODO: 更新数据库
                    # manager.UpdatePerson(person.id, person.name, person.record)
                    self.signTooltipLabel.configure(text="签到成功", foreground='green')
                else:
                    self.signTooltipLabel.configure(text="半小时内只能签到一次", foreground='red')

    # TODO: 需要修改
    def signOut(self):
        if len(self.retInfoList) == 0:
            self.signTooltipLabel.configure(text="没有检测到录入的人脸", foreground='red')
            return
        for info in self.retInfoList:
            info_id, info_name = info[0], info[1]
            person = sqlController.SelectEmployeeBaseInfoById(info_id)
            if person is not None:
                if person.SignOut():
                    # TODO: 更新数据库
                    # manager.UpdatePerson(person.id, person.name, person.record)
                    self.signTooltipLabel.configure(text="签退成功", foreground='green')
                else:
                    self.signTooltipLabel.configure(text="半小时内只能签退一次", foreground='red')

    def addPerson(self):
        # 实现新增人员的逻辑
        InsertWindow(self.master, self.camera)

    def queryPerson(self):
        # 实现查看人员信息的逻辑
        QueryWindow(self.master)

    def modifyPerson(self):
        # 实现修改人员信息的逻辑
        ModifyPersonWindow(self.master)

    def deletePerson(self):
        # 实现删除人员的逻辑
        DeleteWindow(self.master)

    def __del__(self):
        self.camera.release()
        cv2.destroyAllWindows()


class ModifyPersonWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title("修改人员窗口")

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
        # TODO:需要修改
        # self.personToModify = manager.GetPersonById(self.personIdToModify)
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
        # TODO:需要修改
        # manager.UpdatePerson(self.personIdToModify, newName, self.personToModify.record)
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
                # TODO:需要修改
                # manager.UpdatePerson(self.personIdToModify, self.personToModify.name, self.personToModify.record)
                self.resultLabel.configure(text="签到成功", foreground='green')

    def signOut(self):
        # 实现签退逻辑
        if self.checkDateTimeFormat():
            if self.checkPersonExist():
                self.personToModify.SignOutWithTime(self.dateEntry.get(), self.timeEntry.get())
                # TODO:需要修改
                # manager.UpdatePerson(self.personIdToModify, self.personToModify.name, self.personToModify.record)
                self.resultLabel.configure(text="签退成功", foreground='green')


if __name__ == '__main__':
    root = tk.Tk()
    app = MainGUI(root)
    root.geometry("1000x600")
    root.mainloop()
