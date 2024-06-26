import tkinter as tk
from datetime import datetime
from tkinter import ttk, Entry, Label

import cv2
from PIL import Image, ImageTk

from AttendanceSystem.DeleteWindow import DeleteWindow
from AttendanceSystem.InsertWindow import InsertWindow
from AttendanceSystem.QueryWindow import QueryWindow
from AttendanceSystem.ModifyWindow import ModifyWindow
from AttendanceSystem.GUIHelper import UpdateFaceInfoWindow, UpdatePasswordWindow
from FaceRecognition.Recognition import recognition
from SqlController import sqlController


class MainGUI:
    def __init__(self, master):
        self.retInfoList = []  # 保存识别出的人员信息列表[[id, name], ...]
        self.master = master
        master.title("软件界面")

        self.currentUser = None  # 当前登录的用户信息

        # 在顶部居中显示Label
        self.title = ttk.Label(master, text="人脸识别考勤系统界面", font=("", 35), background='white',
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

        # 左侧按钮(管理员版本)
        self.btnAdd = ttk.Button(self.left_frame, text="新增人员", command=self.addPerson, style="TButton")
        self.btnView = ttk.Button(self.left_frame, text="查看人员信息", command=self.queryPerson, style="TButton")
        self.btnEdit = ttk.Button(self.left_frame, text="修改人员信息", command=self.modifyPerson, style="TButton")
        self.btnDelete = ttk.Button(self.left_frame, text="删除人员", command=self.deletePerson, style="TButton")
        self.btnChangeToNormalUser = ttk.Button(self.left_frame, text="切换到普通用户", command=self.changeToNormalUser,
                                                style="TButton")

        self.btnAdd.grid(row=0, column=0, pady=10)
        self.btnView.grid(row=1, column=0, pady=10)
        self.btnEdit.grid(row=2, column=0, pady=10)
        self.btnDelete.grid(row=3, column=0, pady=10)
        self.btnChangeToNormalUser.grid(row=4, column=0, pady=10)

        # 左侧按钮(普通用户版本)
        self.btnSearchMyself = ttk.Button(self.left_frame, text="查询个人信息",
                                          command=self.queryPerson, style="TButton")
        self.btnUpdateFaceInfo = ttk.Button(self.left_frame, text="重新录入人脸信息",
                                            command=self.updateFaceInfo, style="TButton")
        self.btnUpdatePassword = ttk.Button(self.left_frame, text="修改密码",
                                            command=self.updatePassword, style="TButton")

        self.btnSearchMyself.grid(row=0, column=0, pady=10)
        self.btnUpdateFaceInfo.grid(row=1, column=0, pady=10)
        self.btnUpdatePassword.grid(row=2, column=0, pady=10)

        # 登录界面
        self.loginNameLabel = ttk.Label(self.left_frame, text="用户名: ", font=("bold", 15), justify=tk.LEFT)
        self.loginNameEntry = ttk.Entry(self.left_frame, width=20)
        self.loginNameLabel.grid(row=4, column=0, padx=10, pady=10)
        self.loginNameEntry.grid(row=4, column=1, padx=10, pady=10)

        self.loginPasswordLabel = Label(self.left_frame, text=" 密码: ", font=("bold", 15), justify=tk.LEFT)
        self.loginPasswordEntry = Entry(self.left_frame, show='*', width=20)
        self.loginPasswordLabel.grid(row=5, column=0, padx=10, pady=10)
        self.loginPasswordEntry.grid(row=5, column=1, padx=10, pady=10)

        self.loginButton = ttk.Button(self.left_frame, text="人员登录", command=self.login, style="TButton")
        self.loginButton.grid(row=6, column=0, pady=10)

        # 登录失败提示
        self.loginFailLabel = ttk.Label(self.left_frame, text="", foreground='red', font=("", 10))
        self.loginFailLabel.grid(row=6, column=0, pady=10, columnspan=2)

        # 签到签退按钮
        self.signInButton = tk.Button(self.left_frame, text="签到", command=self.signIn, width=12, height=2)
        self.signInButton.grid(row=10, column=0, padx=10, pady=10, sticky=tk.W)
        self.signOutButton = tk.Button(self.left_frame, text="签退", command=self.signOut, width=12, height=2)
        self.signOutButton.grid(row=10, column=1, padx=10, pady=10, sticky=tk.E)

        # 签到提示
        self.signTooltipLabel = ttk.Label(self.left_frame, text="", foreground='red', font=("", 10))
        self.signTooltipLabel.grid(row=7, column=0, pady=10, columnspan=2)

        # 退出登录按钮
        self.logoutButton = ttk.Button(self.left_frame, text="退出登录",
                                       command=self.SetCurrentSection, style="TButton")
        self.logoutButton.grid(row=13, column=0, pady=10, columnspan=2)

        # 默认显示登录界面
        self.SetCurrentSection('login')

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
        # 显示管理员界面
        self.btnAdd.grid(row=0, column=0, pady=10, columnspan=2)
        self.btnView.grid(row=1, column=0, pady=10, columnspan=2)
        self.btnEdit.grid(row=2, column=0, pady=10, columnspan=2)
        self.btnDelete.grid(row=3, column=0, pady=10, columnspan=2)
        self.btnChangeToNormalUser.grid(row=4, column=0, pady=10, columnspan=2)
        self.logoutButton.grid(row=13, column=0, pady=10, columnspan=2)

    def hideManagerSection(self):
        # 隐藏管理员界面
        self.btnAdd.grid_forget()
        self.btnView.grid_forget()
        self.btnEdit.grid_forget()
        self.btnDelete.grid_forget()
        self.btnChangeToNormalUser.grid_forget()
        self.logoutButton.grid_forget()

    def showNormalUserSection(self):
        # 显示普通用户界面
        self.btnSearchMyself.grid(row=0, column=0, pady=10, columnspan=2)
        self.btnUpdateFaceInfo.grid(row=1, column=0, pady=10, columnspan=2)
        self.btnUpdatePassword.grid(row=2, column=0, pady=10, columnspan=2)
        self.logoutButton.grid(row=13, column=0, pady=10, columnspan=2)

    def hideNormalUserSection(self):
        # 隐藏普通用户界面
        self.btnSearchMyself.grid_forget()
        self.btnUpdateFaceInfo.grid_forget()
        self.btnUpdatePassword.grid_forget()
        self.logoutButton.grid_forget()

    def showLoginSection(self):
        # 显示登录界面
        self.loginNameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.loginNameEntry.grid(row=0, column=1, padx=10, pady=10)
        self.loginPasswordLabel.grid(row=1, column=0, padx=1, pady=10)
        self.loginPasswordEntry.grid(row=1, column=1, padx=1, pady=10)
        self.loginButton.grid(row=2, column=0, columnspan=2, pady=10)

    def hideLoginSection(self):
        # 隐藏登录界面
        self.loginNameLabel.grid_forget()
        self.loginNameEntry.grid_forget()
        self.loginPasswordLabel.grid_forget()
        self.loginPasswordEntry.grid_forget()
        self.loginButton.grid_forget()

    def SetCurrentSection(self, section='login'):
        if section == 'manager':
            self.clear()
            self.hideLoginSection()
            self.hideNormalUserSection()
            self.showManagerSection()
        elif section == 'normalUser':
            self.clear()
            self.hideLoginSection()
            self.hideManagerSection()
            self.showNormalUserSection()
        else:  # section == 'login'
            self.clear()
            self.hideManagerSection()
            self.hideNormalUserSection()
            self.showLoginSection()

    def login(self):
        # 实现登录逻辑
        if self.loginNameEntry.get().isspace() or self.loginPasswordEntry.get().isspace() \
                or self.loginNameEntry.get() == '' or self.loginPasswordEntry.get() == '':
            self.loginFailLabel.configure(text="用户名或密码不能为空", foreground='red')
            return
        self.currentUser = sqlController.Login(self.loginNameEntry.get(), self.loginPasswordEntry.get())
        if self.currentUser is not None:
            self.SetCurrentSection("manager" if self.currentUser.userType == 1 else "normalUser")
            self.loginFailLabel.configure(text="")
        else:
            self.loginFailLabel.configure(text="用户名或密码错误", foreground='red')

    def signIn(self):
        if len(self.retInfoList) == 0:
            self.signTooltipLabel.configure(text="没有检测到录入的人脸", foreground='red')
            self.signTooltipLabel.after(5000, lambda: self.signTooltipLabel.configure(text=""))  # 5s后清空
            return
        toolTipText = ""  # 提示信息
        for info in self.retInfoList:
            info_id, info_name = info[0], info[1]
            lastSignInTime = sqlController.GetLastSignInTime(info_id)
            if lastSignInTime is not None and (datetime.now() - lastSignInTime).seconds < 1800:
                toolTipText += f"{info_name}半小时内已签到, 请勿重复签到\n"
            else:
                # 满足签到条件, 进行签到, 并更新数据库
                sqlController.SignIn(info_id)
                toolTipText += f"{info_name}签到成功\n"
        # 提示签到结果
        self.signTooltipLabel.configure(text=toolTipText, foreground='black')
        self.signTooltipLabel.after(10000, lambda: self.signTooltipLabel.configure(text=""))  # 10s后清空

    def signOut(self):
        if len(self.retInfoList) == 0:
            self.signTooltipLabel.configure(text="没有检测到录入的人脸", foreground='red')
            self.signTooltipLabel.after(5000, lambda: self.signTooltipLabel.configure(text=""))
            return
        toolTipText = ""  # 提示信息
        for info in self.retInfoList:
            info_id, info_name = info[0], info[1]
            lastSignOutTime = sqlController.GetLastSignOutTime(info_id)
            if lastSignOutTime is not None and (datetime.now() - lastSignOutTime).seconds < 1800:
                toolTipText += f"{info_name}半小时内已签退, 请勿重复签退\n"
            else:
                # 满足签退条件, 进行签退, 并更新数据库
                sqlController.SignOut(info_id)
                toolTipText += f"{info_name}签退成功\n"
        # 提示签退结果
        self.signTooltipLabel.configure(text=toolTipText, foreground='black')
        self.signTooltipLabel.after(10000, lambda: self.signTooltipLabel.configure(text=""))  # 10s后清空

    def addPerson(self):
        # 实现新增人员的逻辑
        InsertWindow(self.master, self.camera)

    def queryPerson(self):
        # 实现查看人员信息的逻辑
        QueryWindow(self.master, self.currentUser)

    def modifyPerson(self):
        # 实现修改人员信息的逻辑
        ModifyWindow(self.master)

    def deletePerson(self):
        # 实现删除人员的逻辑
        DeleteWindow(self.master, self.currentUser)

    def updateFaceInfo(self):
        # 实现重新录入人脸信息的逻辑
        UpdateFaceInfoWindow(self.currentUser, self.camera)

    def updatePassword(self):
        # 实现修改密码的逻辑
        UpdatePasswordWindow(self.currentUser)

    def changeToNormalUser(self):
        self.currentUser.userType = 0   # 切换到普通用户界面，只在本地修改当前用户的用户类型，不更新数据库
        self.SetCurrentSection('normalUser')

    def clear(self):
        # 清空所有提示和输入框
        self.loginFailLabel.configure(text="")
        self.signTooltipLabel.configure(text="")
        self.loginNameEntry.delete(0, tk.END)
        self.loginPasswordEntry.delete(0, tk.END)

    def __del__(self):
        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainGUI(root)
    root.geometry("1000x700")
    root.mainloop()
